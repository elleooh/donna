"""Base voice handler with shared functionality."""

import json
import base64
import asyncio
import websockets
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
from twilio.rest import Client
from config import (
    OPENAI_API_KEY,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    LOG_EVENT_TYPES,
    SHOW_TIMING_MATH,
)
import traceback
from tools import get_tool_implementation


class BaseVoiceHandler:
    def __init__(self, websocket: WebSocket, agent_manager):
        self.websocket = websocket
        self.agent_manager = agent_manager
        # Initialize with voice connection structure
        self.active_connections = {
            "voice": {
                "ws": None,  # Will be set during handle_media_stream
                "current_agent": None,  # Will be set during handle_media_stream
                "stream_sid": None,
                "latest_media_timestamp": 0,
            }
        }
        self.mark_queue = []
        self.last_assistant_item = None
        self.response_start_timestamp_twilio = None
        self.latest_media_timestamp = 0
        self.stream_sid = None
        self.openai_ws = None
        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    async def receive_from_twilio(self, openai_ws):
        """Receive audio data from Twilio and send it to the OpenAI Realtime API."""
        try:
            async for message in self.websocket.iter_text():
                data = json.loads(message)
                current_ws = self.active_connections.get("voice", {}).get(
                    "ws", openai_ws
                )

                if data["event"] == "media" and current_ws.open:
                    if "voice" in self.active_connections:
                        self.active_connections["voice"]["latest_media_timestamp"] = (
                            int(data["media"]["timestamp"])
                        )
                    audio_append = {
                        "type": "input_audio_buffer.append",
                        "audio": data["media"]["payload"],
                    }
                    await current_ws.send(json.dumps(audio_append))
                elif data["event"] == "start":
                    self.stream_sid = data["start"]["streamSid"]
                    if "voice" in self.active_connections:
                        self.active_connections["voice"]["stream_sid"] = self.stream_sid
                    print(f"Incoming stream has started {self.stream_sid}")
                    self.response_start_timestamp_twilio = None
                    if "voice" in self.active_connections:
                        self.active_connections["voice"]["latest_media_timestamp"] = 0
                    self.last_assistant_item = None
                elif data["event"] == "mark":
                    if self.mark_queue:
                        self.mark_queue.pop(0)
        except WebSocketDisconnect:
            print("Client disconnected.")
            current_ws = self.active_connections.get("voice", {}).get("ws")
            if current_ws and current_ws.open:
                await current_ws.close()

    async def send_to_twilio(self, openai_ws):
        """Receive events from the OpenAI Realtime API, send audio back to Twilio."""
        try:
            while True:  # Keep running even if connection changes
                try:
                    current_ws = self.active_connections.get("voice", {}).get(
                        "ws", openai_ws
                    )
                    async for openai_message in current_ws:
                        response = json.loads(openai_message)
                        if response["type"] in LOG_EVENT_TYPES:
                            print(f"Received event: {response['type']}", response)

                        if (
                            response.get("type")
                            == "response.function_call_arguments.done"
                        ):
                            print("Function call detected in voice stream, handling...")
                            await self.handle_function_call(response, "voice")
                            # Check if connection changed during function call
                            if current_ws != self.active_connections["voice"]["ws"]:
                                print("Connection changed, restarting message loop")
                                break

                        if (
                            response.get("type") == "response.audio.delta"
                            and "delta" in response
                        ):
                            try:
                                audio_payload = base64.b64encode(
                                    base64.b64decode(response["delta"])
                                ).decode("utf-8")
                                audio_delta = {
                                    "event": "media",
                                    "streamSid": self.stream_sid,
                                    "media": {"payload": audio_payload},
                                }
                                await self.websocket.send_json(audio_delta)

                                if self.response_start_timestamp_twilio is None:
                                    self.response_start_timestamp_twilio = (
                                        self.latest_media_timestamp
                                    )
                                    if SHOW_TIMING_MATH:
                                        print(
                                            f"Setting start timestamp for new response: {self.response_start_timestamp_twilio}ms"
                                        )

                                if response.get("item_id"):
                                    self.last_assistant_item = response["item_id"]

                                await self.send_mark()

                            except Exception as e:
                                print(f"Error processing audio data: {e}")

                        if response.get("type") == "input_audio_buffer.speech_started":
                            print("Speech started detected.")
                            if self.last_assistant_item:
                                print(
                                    f"Interrupting response with id: {self.last_assistant_item}"
                                )
                                await self.handle_speech_started_event()

                except websockets.exceptions.ConnectionClosed:
                    print(
                        "WebSocket connection closed, checking if new connection exists"
                    )
                    # If this was an intentional close during agent switching, continue
                    if current_ws != self.active_connections["voice"]["ws"]:
                        continue
                    else:
                        # If this was an unexpected close, raise the exception
                        raise

        except Exception as e:
            print(f"Error in send_to_twilio: {e}")
            traceback.print_exc()
            raise

    async def send_mark(self):
        """Send mark event to Twilio."""
        if self.stream_sid:
            mark_event = {
                "event": "mark",
                "streamSid": self.stream_sid,
                "mark": {"name": "responsePart"},
            }
            await self.websocket.send_json(mark_event)
            self.mark_queue.append("responsePart")

    async def _send_function_result(self, result, call_id):
        """Send function call result back to OpenAI."""
        if isinstance(result, dict):
            result = json.dumps(result)

        result_json = {
            "type": "conversation.item.create",
            "item": {
                "type": "function_call_output",
                "output": result,
                "call_id": call_id,
            },
        }
        try:
            await self.openai_ws.send(json.dumps(result_json))
            await self.openai_ws.send(json.dumps({"type": "response.create"}))
        except Exception as e:
            print(f"Failed to send function call result: {e}")
            traceback.print_exc()

    async def handle_function_call(self, event_json, identifier):
        """Handle function calls from the AI."""
        try:
            ws = self.active_connections[identifier]["ws"]
            current_agent = self.active_connections[identifier]["current_agent"]
            name = event_json.get("name", "")
            call_id = event_json.get("call_id", "")
            arguments = event_json.get("arguments", "{}")
            print(f"Handling function call: {name} with arguments: {arguments}")

            function_call_args = json.loads(arguments)

            if name == "transferAgents":
                new_agent_name = function_call_args["destination_agent"]
                rationale = function_call_args["rationale_for_transfer"]
                context = function_call_args["conversation_context"]

                # Verify routing is allowed using the agent names
                if new_agent_name not in current_agent.get("downstream_agents", []):
                    print(
                        f"Warning: Transfer to {new_agent_name} not allowed from {current_agent['name']}"
                    )
                    return

                new_agent = self.agent_manager.get_agent(new_agent_name)
                if not new_agent:
                    print(f"Warning: Agent {new_agent_name} not found")
                    return

                print(f"Transferring to {new_agent_name} because: {rationale}")
                print(f"Context: {context}")

                # Keep old connection open until new one is ready
                old_ws = ws

                try:
                    # First send success response through old connection
                    result = json.dumps(
                        {
                            "status": "success",
                            "message": f"Transferring to {new_agent_name}: {rationale}",
                        }
                    )
                    result_json = {
                        "type": "conversation.item.create",
                        "item": {
                            "type": "function_call_output",
                            "output": result,
                            "call_id": call_id,
                        },
                    }
                    await old_ws.send(json.dumps(result_json))
                    await old_ws.send(json.dumps({"type": "response.create"}))

                    # Wait a moment for the response to be sent
                    await asyncio.sleep(0.1)

                    # Create new connection with new agent
                    new_ws = await websockets.connect(
                        f"wss://api.openai.com/v1/realtime?model={new_agent['model']}",
                        extra_headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}",
                            "OpenAI-Beta": "realtime=v1",
                        },
                    )

                    # Update active connection before initializing
                    self.active_connections[identifier] = {
                        "ws": new_ws,
                        "current_agent": new_agent,
                        "stream_sid": self.active_connections[identifier].get(
                            "stream_sid"
                        ),
                        "latest_media_timestamp": self.active_connections[
                            identifier
                        ].get("latest_media_timestamp", 0),
                    }

                    # Initialize the new session
                    await self.agent_manager.initialize_session(new_ws, new_agent_name)

                    # Wait for session to be fully initialized
                    await asyncio.sleep(0.2)

                    # Start conversation with new agent
                    initial_message = {
                        "type": "conversation.item.create",
                        "item": {
                            "type": "message",
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_text",
                                    "text": f"Hi, I was transferred here because: {rationale}. Context: {context}",
                                }
                            ],
                        },
                    }
                    await new_ws.send(json.dumps(initial_message))
                    await new_ws.send(json.dumps({"type": "response.create"}))

                    # Close old connection only after new one is confirmed working
                    try:
                        await old_ws.close()
                    except:
                        pass

                    print(f"Successfully switched to {new_agent_name}")
                    return

                except Exception as e:
                    print(f"Error during agent transition: {e}")
                    traceback.print_exc()

                    # Restore old connection if something went wrong
                    self.active_connections[identifier] = {
                        "ws": old_ws,
                        "current_agent": current_agent,
                        "stream_sid": self.active_connections[identifier].get(
                            "stream_sid"
                        ),
                        "latest_media_timestamp": self.active_connections[
                            identifier
                        ].get("latest_media_timestamp", 0),
                    }

                    if "new_ws" in locals():
                        try:
                            await new_ws.close()
                        except:
                            pass
                    return

            # Handle other function calls using the tool registry
            else:
                tool_impl = get_tool_implementation(name)
                if tool_impl:
                    try:
                        result = await tool_impl(**function_call_args)
                        result_json = {
                            "type": "conversation.item.create",
                            "item": {
                                "type": "function_call_output",
                                "output": json.dumps(result),
                                "call_id": call_id,
                            },
                        }
                        await ws.send(json.dumps(result_json))
                        await ws.send(json.dumps({"type": "response.create"}))
                    except Exception as e:
                        print(f"Error executing {name}: {e}")
                        traceback.print_exc()

        except Exception as e:
            print(f"Error handling function call: {e}")
            print(f"Full event_json: {event_json}")
            traceback.print_exc()

    async def handle_speech_started_event(self):
        """Handle interruption when the caller's speech starts."""
        if self.mark_queue and self.response_start_timestamp_twilio is not None:
            elapsed_time = (
                self.latest_media_timestamp - self.response_start_timestamp_twilio
            )
            if SHOW_TIMING_MATH:
                print(
                    f"Calculating elapsed time for truncation: {self.latest_media_timestamp} - {self.response_start_timestamp_twilio} = {elapsed_time}ms"
                )

            if self.last_assistant_item:
                if SHOW_TIMING_MATH:
                    print(
                        f"Truncating item with ID: {self.last_assistant_item}, Truncated at: {elapsed_time}ms"
                    )
                try:
                    # Get current WebSocket connection
                    current_ws = self.active_connections["voice"]["ws"]

                    # Only attempt to send truncate event if connection is still open
                    if current_ws.open:
                        truncate_event = {
                            "type": "conversation.item.truncate",
                            "item_id": self.last_assistant_item,
                            "content_index": 0,
                            "audio_end_ms": elapsed_time,
                        }
                        await current_ws.send(json.dumps(truncate_event))

                    # Send clear event to Twilio
                    await self.websocket.send_json(
                        {"event": "clear", "streamSid": self.stream_sid}
                    )

                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket closed during speech interruption - continuing")
                except Exception as e:
                    print(f"Error during speech interruption: {e}")
                    traceback.print_exc()

            self.mark_queue.clear()
            self.last_assistant_item = None
            self.response_start_timestamp_twilio = None

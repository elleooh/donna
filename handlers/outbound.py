"""Outbound voice call handler: Agent Donna reach out to human recruiter for offer negotiation with competing offers"""

import json
import asyncio
import websockets
from twilio.rest import Client
from config import (
    OPENAI_API_KEY,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    PHONE_NUMBER_FROM,
    DOMAIN,
    SYSTEM_MESSAGE,
)
from .base import BaseVoiceHandler


class OutboundVoiceHandler(BaseVoiceHandler):
    async def handle_media_stream(self):
        """Main handler for outbound voice media stream."""
        await self.websocket.accept()
        print("Outbound client connected")

        try:
            # Get initial OpenAI connection
            initial_agent = self.agent_manager.get_agent("main_agent")
            self.openai_ws = await websockets.connect(
                f"wss://api.openai.com/v1/realtime?model={initial_agent['model']}",
                extra_headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "OpenAI-Beta": "realtime=v1",
                },
            )

            # Initialize active connections
            self.active_connections["voice"] = {
                "ws": self.openai_ws,
                "current_agent": initial_agent,
                "stream_sid": None,
                "latest_media_timestamp": 0,
            }

            # Initialize session
            await self._initialize_session()

            # Start bidirectional communication
            await self._handle_stream()

        except Exception as e:
            print(f"Error in outbound media stream: {e}")
            if self.openai_ws and not self.openai_ws.closed:
                await self.openai_ws.close()
            raise

    async def _initialize_session(self):
        """Initialize OpenAI session for outbound call."""
        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": "alloy",
                "instructions": SYSTEM_MESSAGE,
                "modalities": ["text", "audio"],
                "temperature": 0.8,
            },
        }
        print("Sending session update:", session_update)
        await self.openai_ws.send(json.dumps(session_update))

        # Have the AI speak first
        await self._send_initial_greeting()

    async def _send_initial_greeting(self):
        """Send initial conversation so AI talks first."""
        initial_conversation_item = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Greet the user with 'Hello! This is {name} calling. I recently got offer from you for the position of {job_title}. I hope I'm not catching you at a bad time? How are you doing today?'"
                        ),
                    }
                ],
            },
        }
        await self.openai_ws.send(json.dumps(initial_conversation_item))
        await self.openai_ws.send(json.dumps({"type": "response.create"}))

    async def _handle_stream(self):
        """Handle bidirectional stream between Twilio and OpenAI."""
        try:
            # Create tasks for receiving from Twilio and sending to Twilio
            receive_task = self.receive_from_twilio(self.openai_ws)
            send_task = self.send_to_twilio(self.openai_ws)

            # Run both tasks concurrently
            await asyncio.gather(receive_task, send_task)

        except Exception as e:
            print(f"Error in stream handling: {e}")
            if not isinstance(e, websockets.exceptions.ConnectionClosed):
                raise

    async def make_call(self, phone_number: str):
        """Initiate an outbound call."""
        if not phone_number:
            raise ValueError("Please provide a phone number to call.")

        is_allowed = await self.check_number_allowed(phone_number)
        if not is_allowed:
            raise ValueError(
                f"The number {phone_number} is not recognized as a valid outgoing number or caller ID."
            )

        outbound_twiml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<Response><Connect><Stream url="wss://{DOMAIN}/media-stream-outbound" /></Connect></Response>'
        )

        call = self.twilio_client.calls.create(
            from_=PHONE_NUMBER_FROM, to=phone_number, twiml=outbound_twiml
        )

        print(f"Call started with SID: {call.sid}")
        return call.sid

    async def check_number_allowed(self, to: str) -> bool:
        """Check if a number is allowed to be called."""
        try:
            # Add numbers you have permission to call
            OVERRIDE_NUMBERS = []  # Add to config
            if to in OVERRIDE_NUMBERS:
                return True

            incoming_numbers = self.twilio_client.incoming_phone_numbers.list(
                phone_number=to
            )
            if incoming_numbers:
                return True

            outgoing_caller_ids = self.twilio_client.outgoing_caller_ids.list(
                phone_number=to
            )
            if outgoing_caller_ids:
                return True

            return False
        except Exception as e:
            print(f"Error checking phone number: {e}")
            return False

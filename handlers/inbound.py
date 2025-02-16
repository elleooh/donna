"""Inbound voice call handler: Human recruiter reach out to Donna to provide offer; Donna will provide information about the candidate"""

import asyncio
import websockets
from config import OPENAI_API_KEY
from .base import BaseVoiceHandler


class InboundVoiceHandler(BaseVoiceHandler):
    async def handle_media_stream(self):
        """Main handler for inbound voice media stream."""
        await self.websocket.accept()
        print("Inbound client connected")

        try:
            # Get initial OpenAI connection for main agent
            initial_agent = self.agent_manager.get_agent("main_agent")
            self.openai_ws = await websockets.connect(
                f"wss://api.openai.com/v1/realtime?model={initial_agent['model']}",
                extra_headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "OpenAI-Beta": "realtime=v1",
                },
            )

            # Initialize active connections with main agent
            self.active_connections["voice"] = {
                "ws": self.openai_ws,
                "current_agent": initial_agent,
                "stream_sid": None,
                "latest_media_timestamp": 0,
            }

            # Initialize the session
            await self.agent_manager.initialize_session(self.openai_ws, "main_agent")

            # Start bidirectional communication
            await self._handle_stream()

        except Exception as e:
            print(f"Error in inbound media stream: {e}")
            if self.openai_ws and not self.openai_ws.closed:
                await self.openai_ws.close()
            raise

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

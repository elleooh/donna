"""Voice stream handling logic."""

import json
import base64
import websockets
from config import OPENAI_API_KEY, SHOW_TIMING_MATH
from tools import get_tool_implementation


class VoiceHandler:
    def __init__(self, websocket, agent_manager):
        self.websocket = websocket
        self.agent_manager = agent_manager
        self.active_connections = {}
        self.mark_queue = []
        self.last_assistant_item = None
        self.response_start_timestamp_twilio = None
        self.latest_media_timestamp = 0
        self.stream_sid = None

    async def handle_media_stream(self):
        """Main handler for voice media stream."""
        async with websockets.connect(
            f"wss://api.openai.com/v1/realtime?model={self.agent_manager.get_agent('main_agent')['model']}",
            extra_headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "OpenAI-Beta": "realtime=v1",
            },
        ) as openai_ws:
            await self._initialize_voice_session(openai_ws)
            await self._handle_stream(openai_ws)

    async def handle_function_call(self, event_json):
        """Handle function calls from the AI."""
        name = event_json.get("name", "")
        call_id = event_json.get("call_id", "")
        arguments = json.loads(event_json.get("arguments", "{}"))

        if name == "transferAgents":
            # Handle transfer logic
            pass
        else:
            # Handle other function calls using the tool registry
            tool_impl = get_tool_implementation(name)
            if tool_impl:
                result = await tool_impl(**arguments)
                await self._send_function_result(result, call_id)

    # ... rest of voice handling methods ...

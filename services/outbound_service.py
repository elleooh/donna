"""FastAPI service for handling outbound voice calls."""

import argparse
from fastapi import FastAPI, WebSocket, BackgroundTasks
from fastapi.responses import JSONResponse
from handlers.outbound import OutboundVoiceHandler
from agents.manager import AgentManager
from config import OUTBOUND_PORT

app = FastAPI()
agent_manager = AgentManager()


@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}


@app.websocket("/media-stream-outbound")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections for outbound calls."""
    handler = OutboundVoiceHandler(websocket, agent_manager)
    await handler.handle_media_stream()


@app.post("/outbound-call/{phone_number}")
async def initiate_outbound_call(phone_number: str, background_tasks: BackgroundTasks):
    """Initiate an outbound call to the specified phone number."""
    handler = OutboundVoiceHandler(None, agent_manager)
    call_sid = await handler.make_call(phone_number)
    return {"message": "Call initiated", "call_sid": call_sid}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the Twilio AI voice assistant server."
    )
    parser.add_argument(
        "--call",
        required=True,
        help="The phone number to call, e.g., '--call=+18005551212'",
    )
    args = parser.parse_args()

    phone_number = args.call
    print(
        "Our recommendation is to always disclose the use of AI for outbound or inbound calls.\n"
        "Reminder: All of the rules of TCPA apply even if a call is made by AI.\n"
        "Check with your counsel for legal and compliance advice."
    )

    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(initiate_outbound_call(phone_number, None))

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=OUTBOUND_PORT)

"""FastAPI service for handling inbound voice calls."""

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from twilio.twiml.voice_response import VoiceResponse, Connect
from handlers.inbound import InboundVoiceHandler
from agents.manager import AgentManager
from config import INBOUND_PORT

app = FastAPI()
agent_manager = AgentManager()


@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}


@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    """Handle incoming call and return TwiML response."""
    response = VoiceResponse()
    response.say("Please wait")
    response.pause(length=1)

    # Get the host from the request
    host = request.url.hostname

    # Set up media stream
    connect = Connect()
    connect.stream(url=f"wss://{host}/media-stream")
    response.append(connect)

    return HTMLResponse(content=str(response), media_type="application/xml")


@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    """Handle WebSocket connections for inbound calls."""
    handler = InboundVoiceHandler(websocket, agent_manager)
    await handler.handle_media_stream()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=INBOUND_PORT)

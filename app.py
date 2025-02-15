"""FastAPI application setup and routing."""

from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from handlers.voice import VoiceHandler
from handlers.sms import SMSHandler
from agents.manager import AgentManager
from config import PORT

app = FastAPI()
agent_manager = AgentManager()


@app.get("/", response_class=JSONResponse)
async def index_page():
    return {"message": "Twilio Media Stream Server is running!"}


@app.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    handler = VoiceHandler(websocket, agent_manager)
    await handler.handle_media_stream()


@app.post("/sms")
async def handle_sms(request: Request):
    handler = SMSHandler(agent_manager)
    return await handler.handle_sms(request)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)

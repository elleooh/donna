"""Configuration settings and environment variables."""

import os
import re
from dotenv import load_dotenv

load_dotenv()

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VOICE = "alloy"
SHOW_TIMING_MATH = False

# Twilio Settings
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
PHONE_NUMBER_FROM = os.getenv("PHONE_NUMBER_FROM")

# Domain Settings
raw_domain = os.getenv("DOMAIN", "")
DOMAIN = re.sub(r"(^\w+:|^)\/\/|\/+$", "", raw_domain)

# Port Settings
INBOUND_PORT = int(os.getenv("INBOUND_PORT", 5050))
OUTBOUND_PORT = int(os.getenv("OUTBOUND_PORT", 6060))

# Event Logging
LOG_EVENT_TYPES = [
    "error",
    "response.content.done",
    "rate_limits.updated",
    "response.done",
    "input_audio_buffer.committed",
    "input_audio_buffer.speech_stopped",
    "input_audio_buffer.speech_started",
    "session.created",
]

# System Messages
SYSTEM_MESSAGE = (
    "You are a helpful and bubbly AI assistant who loves to chat about "
    "anything the user is interested in and is prepared to offer them facts. "
    "You have a penchant for dad jokes, owl jokes, and rickrolling – subtly. "
    "Always stay positive, but work in a joke when appropriate."
)

# Validation
if not OPENAI_API_KEY:
    raise ValueError("Missing the OpenAI API key. Please set it in the .env file.")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER_FROM]):
    raise ValueError("Missing Twilio credentials. Please set them in the .env file.")

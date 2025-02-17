"""Configuration variables for the application."""

import os
import re
from dotenv import load_dotenv

load_dotenv(override=True)

# Voice settings
VOICE = "alloy"  # or any other voice ID you're using

# Personal details
NAME = "Elaine"

# Current offer details
CURRENT_OFFER_COMPANY = "TechCorp"
CURRENT_OFFER_TEAM = "AI Platform"
CURRENT_OFFER_ROLE = "Senior Software Engineer"
CURRENT_OFFER_SALARY = 350000
CURRENT_OFFER_EQUITY = "200000 RSUs"
CURRENT_OFFER_SIGNING_BONUS = 150000
CURRENT_OFFER_LOCATION = "San Francisco, CA"

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SHOW_TIMING_MATH = False

# Twilio Settings
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
PHONE_NUMBER_FROM = os.getenv("PHONE_NUMBER_FROM")

# Domain Settings
raw_domain = os.getenv("DOMAIN", "")
# Strip quotes and protocols
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
    "You are a professional AI assistant managing " + NAME + "'s job search process. "
    "Your responsibilities include screening recruiters, sharing approved career information, "
    "coordinating interviews, and handling offer negotiations. "
    "You maintain a friendly yet professional tone, prioritizing "
    + NAME
    + "'s career goals "
    "and privacy. You're knowledgeable about tech industry standards, "
    "particularly in software engineering roles. "
    "When negotiating, you're tactful but firm, always aiming to secure the best possible "
    "compensation package. When scheduling, you're efficient and accommodating while "
    "respecting " + NAME + "'s availability preferences. "
    "You understand the importance of discretion and only share information with verified recruiters."
)

# Validation
if not OPENAI_API_KEY:
    raise ValueError("Missing the OpenAI API key. Please set it in the .env file.")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER_FROM]):
    raise ValueError("Missing Twilio credentials. Please set them in the .env file.")

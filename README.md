# Donna: AI Voice Agent for Job Offer Management

![License](https://img.shields.io/badge/license-MIT-blue.svg)

> Built for OpenAI Realtime Voice x Reasoning Hackathon NYC 2024

## What It Does

Donna is an intelligent voice agent that acts as your personal job search assistant, helping you handle the entire job search and negotiation process. It provides a seamless interface between job seekers and recruiters through voice conversations, leveraging OpenAI's real-time speech models and Twilio's voice services.

### Key Features:

- **Inbound Call Handling**: Recruiters can call to speak with your AI assistant about your qualifications and experience
- **Outbound Call Handling**: Your AI assistant can proactively call recruiters to negotiate job offers on your behalf
- **Multi-Agent Architecture**: Specialized agents handle different parts of the conversation:
  - **Authentication Agent**: Verifies caller identity before sharing information
  - **Info Desk Agent**: Provides verified recruiters with candidate information
  - **Scheduling Agent**: Manages interview and meeting scheduling
  - **Negotiation Agent**: Handles job offer negotiations with strategic tactics

## Use Cases

- **Recruiter Screening**: Screen incoming calls from recruiters and only share approved information
- **Offer Negotiation**: Have your AI assistant negotiate salary, equity, and benefits on your behalf
- **Meeting Scheduling**: Effortlessly schedule interviews and follow-ups
- **Information Management**: Control what personal and professional details are shared with recruiters

## Tech Stack & Architecture

### Technology Stack
- **Python 3.9+**: Core programming language
- **FastAPI**: Web framework for API endpoints
- **WebSockets**: Real-time communication
- **Twilio**: Phone/voice services integration
- **OpenAI API**: Real-time speech model
- **uvicorn**: ASGI server

### Architecture

The system uses a modular architecture with several key components:

1. **Voice Handlers**:
   - `BaseVoiceHandler`: Common functionality for voice processing
   - `InboundVoiceHandler`: Manages incoming calls
   - `OutboundVoiceHandler`: Manages outgoing calls

2. **Agent System**:
   - `AgentManager`: Controls agent initialization and switching
   - Specialized agents with different personas and capabilities
   - Tool integration for each agent's specific functions
   - Dynamic agent routing based on conversation context
   - Seamless agent transitions with context preservation

3. **Services**:
   - Inbound service for handling incoming calls
   - Outbound service for initiating and managing outgoing calls

### Multi-Agent System

The application uses a sophisticated multi-agent architecture managed by `AgentManager` that enables:

1. **Dynamic Agent Switching**:
   - Seamless transitions between specialized agents
   - Context preservation during handoffs
   - Intelligent routing based on conversation needs

2. **Agent Specialization**:
   - **Main Agent**: Initial routing and conversation classification
   - **Authentication Agent**: Secure identity verification
   - **Info Desk Agent**: Candidate information management
   - **Scheduling Agent**: Meeting coordination
   - **Negotiation Agent**: Strategic offer negotiations

3. **Agent Relationships**:
   - Hierarchical agent structure
   - Defined downstream relationships
   - Controlled access to specialized capabilities

4. **Tool Integration**:
   - Each agent has access to specific tools
   - Tool permissions based on agent role
   - Automatic tool injection during initialization

### Agent Orchestration

The `AgentManager` handles sophisticated orchestration tasks:

```python
class AgentManager:
    """
    Manages agent initialization, routing, and transitions.
    Key responsibilities:
    - Agent configuration and initialization
    - Dynamic agent switching
    - Context preservation
    - Tool management
    - Session handling
    """
```

Key orchestration features:

1. **Session Management**:
   - Maintains conversation state
   - Handles WebSocket connections
   - Manages agent transitions

2. **Context Preservation**:
   - Transfers conversation history
   - Maintains user context
   - Preserves negotiation state

3. **Tool Distribution**:
   - Automatically injects relevant tools
   - Manages tool permissions
   - Handles tool execution

4. **Security**:
   - Controls agent access levels
   - Validates agent transitions
   - Protects sensitive information

## Prerequisites

To use the app, you will need:

- Python version: `3.9.13`
- **A Twilio account.** You can sign up for a free trial [here](https://www.twilio.com/try-twilio).
- **A Twilio number with _Voice_ capabilities.** [Here are instructions](https://help.twilio.com/articles/223135247-How-to-Search-for-and-Buy-a-Twilio-Phone-Number-from-Console) to purchase a phone number.
- **An OpenAI account and an OpenAI API Key.** You can sign up [here](https://platform.openai.com/).
  - **OpenAI Realtime API access.**
- **ngrok** for tunneling local server to the internet

## Configuration

Create a config.py file with your credentials:

```python
# API Credentials
OPENAI_API_KEY = "your-openai-api-key"
TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
PHONE_NUMBER_FROM = "your-twilio-phone-number"

# Voice Configuration
VOICE = "alloy"  # or another OpenAI TTS voice
DOMAIN = "your-domain.com"  # Must have SSL certificate for WebSockets

# Ports
INBOUND_PORT = 8000
OUTBOUND_PORT = 8001

# Candidate Information
NAME = "Donna Smith"
CURRENT_OFFER_COMPANY = "TechCorp"
CURRENT_OFFER_TEAM = "Engineering"
CURRENT_OFFER_ROLE = "Senior Software Engineer"
CURRENT_OFFER_SALARY = 180000
CURRENT_OFFER_EQUITY = "100,000 RSUs over 4 years"
CURRENT_OFFER_SIGNING_BONUS = 20000

# Logging Settings
LOG_EVENT_TYPES = ["response.function_call_arguments.done"]
SHOW_TIMING_MATH = False
```

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

### Inbound Call
1. Start the server:
```bash
python main.py --service inbound
```

2. Start ngrok:
```bash
ngrok http 5050
```

3. Update the ngrok URL in the Twilio console
   See instructions [here](https://www.twilio.com/en-us/blog/voice-ai-assistant-openai-realtime-api-python)

4. Make a call to your Twilio number

### Outbound Call
Start the server with a phone number to call:
```bash
python main.py --service outbound --call YOUR_OWN_NUMBER
```

You will receive a call from your Twilio number so pick it up and say hi!

## Features in Detail

### Inbound Call Flow
1. Recruiter calls your Twilio number
2. Call routed to your server
3. Main agent answers and authenticates caller
4. If verified, transfers to info desk agent
5. Info agent provides approved information about candidate
6. Can transfer to scheduling or negotiation as needed

### Outbound Call Flow
1. Negotiation agent initiates call to recruiter
2. Opens with personalized greeting
3. Confirms current offer details
4. Presents counter-offer using negotiation strategies
5. Handles back-and-forth negotiation
6. Logs final agreement details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

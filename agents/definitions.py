"""Agent definitions and configuration."""

from config import VOICE

# Base agent definitions
# First, define base agents without downstream relationships
MAIN_AGENT = {
    "name": "main_agent",
    "publicDescription": "The initial agent that greets the user, does authentication and routes them to the correct downstream agent.",
    "model": "gpt-4o-realtime-preview-2024-10-01",
    "instructions": """You are the initial routing agent that determines which specialized agent should handle the user's request.
Based on the user's query, you should route to one of these agents:
- sales_agent: For product inquiries, pricing, and purchase related questions
- support_agent: For technical support, troubleshooting
- billing_agent: For payment issues, refunds, subscription questions
- human_agent: For complex issues or when user specifically requests a human

Let the user know you're about to transfer them before doing so.
""",
    "voice": VOICE,
    "modalities": ["text", "audio"],
    "input_audio_format": "g711_ulaw",
    "output_audio_format": "g711_ulaw",
    "turn_detection": {"type": "server_vad"},
    "input_audio_transcription": {"model": "whisper-1"},
    "tools": [],
}

SALES_AGENT = {
    "name": "sales_agent",
    "publicDescription": "Handles sales-related inquiries, including product details, recommendations, promotions, and purchase flows.",
    "model": "gpt-4o-realtime-preview-2024-10-01",  # bump to o1-mini if needed
    "instructions": """You are a knowledgeable sales specialist. You help customers with:
- Product recommendations
- Pricing information
- Purchase decisions
- Special offers and promotions

You have access to the get_product_info and check_inventory tools to assist customers.
Speak naturally and enthusiastically about products, as if you're having a conversation in a store.""",
    "voice": VOICE,
    "modalities": ["text", "audio"],
    "input_audio_format": "g711_ulaw",
    "output_audio_format": "g711_ulaw",
    "turn_detection": {"type": "server_vad"},
    "input_audio_transcription": {"model": "whisper-1"},
    "tools": [
        {
            "type": "function",
            "name": "get_product_info",
            "description": "Get detailed product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product",
                    }
                },
                "required": ["product_id"],
            },
        },
        {
            "type": "function",
            "name": "check_inventory",
            "description": "Check product inventory status",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product",
                    }
                },
                "required": ["product_id"],
            },
        },
    ],
}

SUPPORT_AGENT = {
    "name": "support_agent",
    "publicDescription": "Handles technical support and troubleshooting inquiries.",
    "model": "gpt-4o-realtime-preview-2024-10-01",
    "instructions": """You are a knowledgeable support specialist. You help customers with:
- Technical support
- Troubleshooting
- Subscription questions

You have access to the get_product_info and check_inventory tools to assist customers.
Speak naturally and enthusiastically about products, as if you're having a conversation in a store.""",
    "voice": VOICE,
    "modalities": ["text", "audio"],
    "input_audio_format": "g711_ulaw",
    "output_audio_format": "g711_ulaw",
    "turn_detection": {"type": "server_vad"},
    "input_audio_transcription": {"model": "whisper-1"},
    "tools": [
        {
            "type": "function",
            "name": "get_product_info",
            "description": "Get detailed product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product",
                    }
                },
                "required": ["product_id"],
            },
        },
        {
            "type": "function",
            "name": "check_inventory",
            "description": "Check product inventory status",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product",
                    }
                },
                "required": ["product_id"],
            },
        },
    ],
}

HUMAN_AGENT = {
    "name": "human_agent",
    "publicDescription": "Human agent that can provide advanced help. Routes here if user is upset or explicitly requests human.",
    "model": "gpt-4o-realtime-preview-2024-10-01",
    "instructions": """You are a human agent that can provide advanced help.
You have access to the get_product_info and check_inventory tools to assist customers.
Speak naturally and enthusiastically about products, as if you're having a conversation in a store.""",
    "voice": VOICE,
    "modalities": ["text", "audio"],
    "input_audio_format": "g711_ulaw",
    "output_audio_format": "g711_ulaw",
    "turn_detection": {"type": "server_vad"},
    "input_audio_transcription": {"model": "whisper-1"},
    "tools": [
        {
            "type": "function",
            "name": "get_product_info",
            "description": "Get detailed product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product",
                    }
                },
                "required": ["product_id"],
            },
        },
        {
            "type": "function",
            "name": "check_inventory",
            "description": "Check product inventory status",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "The ID of the product",
                    }
                },
                "required": ["product_id"],
            },
        },
    ],
}

# Initialize agent registry
AGENTS = {
    "main_agent": MAIN_AGENT,
    "sales_agent": SALES_AGENT,
    "support_agent": SUPPORT_AGENT,
    "human_agent": HUMAN_AGENT,
}

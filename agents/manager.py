"""Agent management and initialization logic."""

from agents.definitions import (
    MAIN_AGENT,
    AUTHENTICATION_AGENT,
    INFO_DESK_AGENT,
    SCHEDULING_AGENT,
    NEGOTIATION_AGENT,
    REASONING_AGENT
)
from tools import get_tools_for_agent
import json
from config import VOICE


class AgentManager:
    def __init__(self):
        self.agents = {}
        self.current_agent_name = "main_agent"
        self.current_conversation_context = None
        self.setup_agents()

    def setup_agents(self):
        """Initialize agents and their relationships."""
        # Setup base agents
        base_agents = [
            MAIN_AGENT,
            AUTHENTICATION_AGENT,
            INFO_DESK_AGENT,
            SCHEDULING_AGENT,
            NEGOTIATION_AGENT,
            REASONING_AGENT
        ]

        # Create initial agent dictionary for reference
        self.agents = {agent["name"]: agent for agent in base_agents}

        # Setup relationships
        self._setup_agent_relationships()

        # Add tools to agents
        for agent in base_agents:
            agent["tools"] = get_tools_for_agent(agent["name"])

        # Inject transfer tools and update agents dictionary
        self.agents = {
            agent["name"]: agent for agent in self._inject_transfer_tools(base_agents)
        }

    def _setup_agent_relationships(self):
        """Define downstream relationships between agents."""
        MAIN_AGENT["downstream_agents"] = [
            "authentication_agent",
            "info_desk_agent",
            "scheduling_agent",
            "negotiation_agent",
            "reasoning_agent"
        ]
        AUTHENTICATION_AGENT["downstream_agents"] = [
            "main_agent",
            "info_desk_agent",
            "scheduling_agent",
        ]
        INFO_DESK_AGENT["downstream_agents"] = [
            "main_agent",
            "scheduling_agent",
        ]
        NEGOTIATION_AGENT["downstream_agents"] = [
            "reasoning_agent",
            "scheduling_agent",  # TODO: if there is follow up conversation
        ]

    def _inject_transfer_tools(self, agent_defs):
        """Inject transfer tools into each agent based on their downstream agents."""
        for agent in agent_defs:
            downstream_agents = agent.get("downstream_agents", [])
            if downstream_agents:
                # Build available agents list for the prompt using self.agents
                available_agents_list = "\n".join(
                    [
                        f"- {name}: {self.agents[name].get('publicDescription', 'No description')}"
                        for name in downstream_agents
                    ]
                )

                # Create the transferAgents tool
                transfer_tool = {
                    "type": "function",
                    "name": "transferAgents",
                    "description": f"""Triggers a transfer of the user to a more specialized agent.
Calls escalate to a more specialized LLM agent or to a human agent, with additional context.
Only call this function if one of the available agents is appropriate.
Don't transfer to your own agent type.

Let the user know you're thinking and need a minute them before doing so.

Available Agents:
{available_agents_list}
                    """,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rationale_for_transfer": {
                                "type": "string",
                                "description": "The reasoning why this transfer is needed.",
                            },
                            "conversation_context": {
                                "type": "string",
                                "description": "Relevant context from the conversation that will help the recipient perform the correct action.",
                            },
                            "destination_agent": {
                                "type": "string",
                                "description": "The more specialized destination_agent that should handle the user's intended request.",
                                "enum": downstream_agents,
                            },
                        },
                        "required": [
                            "rationale_for_transfer",
                            "conversation_context",
                            "destination_agent",
                        ],
                    },
                }

                # Add transfer tool to agent's tools
                if not agent.get("tools"):
                    agent["tools"] = []
                agent["tools"].append(transfer_tool)

        return agent_defs

    def get_agent(self, agent_name):
        """Get agent configuration by name."""
        return self.agents.get(agent_name)

    async def initialize_session(self, openai_ws, agent_name: str):
        """Initialize an OpenAI session for an agent."""
        agent_config = self.get_agent(agent_name)
        if not agent_config:
            raise ValueError(f"Agent {agent_name} not found")

        # First, send the basic session update
        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": agent_config.get(
                    "turn_detection", {"type": "server_vad"}
                ),
                "input_audio_format": agent_config.get(
                    "input_audio_format", "g711_ulaw"
                ),
                "output_audio_format": agent_config.get(
                    "output_audio_format", "g711_ulaw"
                ),
                "voice": agent_config.get("voice", VOICE),
                "instructions": agent_config["instructions"],
                "modalities": agent_config.get("modalities", ["text", "audio"]),
                "temperature": 0.8,
                "input_audio_transcription": agent_config.get(
                    "input_audio_transcription", {"model": "whisper-1"}
                ),
                "tool_choice": "auto",
                "tools": agent_config["tools"],
            },
        }
        print("Sending voice session update:", json.dumps(session_update))
        await openai_ws.send(json.dumps(session_update))

        # Then, immediately send an initial conversation item to set context
        context_message = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": agent_config["instructions"],
                    }
                ],
            },
        }
        await openai_ws.send(json.dumps(context_message))

        # Send a commit message to ensure the context is processed
        await openai_ws.send(json.dumps({"type": "response.create"}))

        # If there's transfer context, send it after initialization
        if self.current_conversation_context:
            transfer_message = {
                "type": "conversation.item.create",
                "item": {
                    "type": "message",
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": self.current_conversation_context,
                        }
                    ],
                },
            }
            await openai_ws.send(json.dumps(transfer_message))
            await openai_ws.send(json.dumps({"type": "response.create"}))
            self.current_conversation_context = None

    async def get_openai_connection(self, agent_name: str):
        """Get a new OpenAI connection for an agent."""
        agent = self.get_agent(agent_name)
        if not agent:
            raise ValueError(f"Agent {agent_name} not found")

        self.current_agent_name = agent_name
        return agent

"""Agent management and initialization logic."""

from agents.definitions import MAIN_AGENT, SALES_AGENT, SUPPORT_AGENT, HUMAN_AGENT
from tools import get_tools_for_agent
import json
from config import SYSTEM_MESSAGE, VOICE


class AgentManager:
    pass  # TODO: in charge of setting up agents and agent routing

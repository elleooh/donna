"""Tool registration and management."""

from typing import Dict, Callable, Awaitable, Any
from tools.authentication import verifyRecruiterCredentials

from tools.info_tesk import lookupCareerInfo, logRecruiterRequest
from tools.scheduling import returnAvailableDateTime, scheduleMeeting
from tools.negotiation import checkCurrentOffer, checkIndustrySalary, logFinalOffer
from agents.definitions import ALLOWED_CAREER_FIELDS

# Tool registry mapping function names to implementations
TOOL_REGISTRY = {
    "verifyRecruiterCredentials": verifyRecruiterCredentials,
    "lookupCareerInfo": lookupCareerInfo,
    "logRecruiterRequest": logRecruiterRequest,
    "returnAvailableDateTime": returnAvailableDateTime,
    "scheduleMeeting": scheduleMeeting,
    "checkCurrentOffer": checkCurrentOffer,
    "checkIndustrySalary": checkIndustrySalary,
    "logFinalOffer": logFinalOffer,
}


def get_tool_implementation(name: str) -> Callable[..., Awaitable[Any]]:
    """Get the implementation for a tool by name."""
    return TOOL_REGISTRY.get(name)


# Tool definitions for agents
AUTHENTICATION_TOOLS = [
    {
        "type": "function",
        "name": "verifyRecruiterCredentials",
        "description": "Verifies the recruiter's credentials against our database",
        "parameters": {
            "type": "object",
            "properties": {
                "fullName": {
                    "type": "string",
                    "description": "Recruiter's full name",
                },
                "company": {
                    "type": "string",
                    "description": "Recruiting company name",
                },
                "position": {
                    "type": "string",
                    "description": "Job position being discussed",
                },
            },
            "required": ["fullName", "company", "position"],
        },
    }
]

INFO_DESK_TOOLS = [
    {
        "type": "function",
        "name": "lookupCareerInfo",
        "description": "Retrieves career aspirations, workexperience, education, skills, and availability for verified recruiters",
        "parameters": {
            "type": "object",
            "properties": {
                "requestedFields": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ALLOWED_CAREER_FIELDS,
                    },
                    "description": "List of information fields being requested",
                },
            },
            "required": ["requestedFields"],
        },
    },
    {
        "type": "function",
        "name": "logRecruiterRequest",
        "description": "Logs the recruiter's and the potential role information request to a text file",
        "parameters": {
            "type": "object",
            "properties": {
                "recruiterName": {
                    "type": "string",
                    "description": "Verified recruiter's name",
                },
                "company": {
                    "type": "string",
                    "description": "The company the recruiter is representing",
                },
                "potentialRole": {
                    "type": "string",
                    "description": "The role the recruiter is looking for",
                },
                "potentialRoleDescription": {
                    "type": "string",
                    "description": "A description of the role the recruiter is looking for",
                },
                "expectedSalaryRange": {
                    "type": "string",
                    "description": "The expected salary range the recruiter is looking for",
                },
                "expectedLocation": {
                    "type": "string",
                    "description": "The location the recruiter is looking for",
                },
                "sponsorVisa": {
                    "type": "boolean",
                    "description": "Whether the company is sponsoring a visa",
                },
                "interviewTimeline": {
                    "type": "string",
                    "description": "The timeline for the interview process",
                },
                "interviewProcess": {
                    "type": "string",
                    "description": "The interview process for the role",
                },
            },
            "required": ["recruiterName", "company", "potentialRole"],
        },
    },
]

SCHEDULING_TOOLS = [
    {
        "type": "function",
        "name": "returnAvailableDateTime",
        "description": "Returns available dates/times for the next two weeks.",
        "parameters": {
            "type": "object",
            "properties": {
                "suggestedDates": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Date and time in ISO format",
                    },
                    "description": "Optional list of interview dates/times suggested",
                },
                "duration": {
                    "type": "number",
                    "description": "Meeting duration in minutes",
                },
                "timeZone": {
                    "type": "string",
                    "description": "Meeting time zone",
                },
            },
            "required": ["duration", "timeZone"],
        },
    },
    {
        "type": "function",
        "name": "scheduleMeeting",
        "description": "Creates a calendar invite for the meeting",
        "parameters": {
            "type": "object",
            "properties": {
                "dateTime": {
                    "type": "string",
                    "description": "Meeting start time in ISO format",
                },
                "duration": {
                    "type": "number",
                    "description": "Meeting duration in minutes",
                },
                "format": {
                    "type": "string",
                    "enum": ["video", "phone"],
                    "description": "Meeting format",
                },
                "participantName": {
                    "type": "string",
                    "description": "Meeting participant's name",
                },
                "participantOrg": {
                    "type": "string",
                    "description": "Meeting participant's organization (if applicable)",
                },
                "participantEmail": {
                    "type": "string",
                    "description": "Meeting participant's email",
                },
                "meetingType": {
                    "type": "string",
                    "enum": [
                        "general_meeting",
                        "initial_screening",
                        "technical_discussion",
                        "team_interview",
                        "final_round",
                        "follow_up",
                    ],
                    "description": "Type of meeting",
                },
                "notes": {
                    "type": "string",
                    "description": "Additional meeting notes or agenda",
                },
            },
            "required": [
                "dateTime",
                "duration",
                "format",
                "participantName",
                "participantOrg",
                "participantEmail",
                "meetingType",
            ],
        },
    },
]

NEGOTIATION_TOOLS = [
    {
        "type": "function",
        "name": "checkCurrentOffer",
        "description": "Checks the details of the current offer",
        "parameters": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "company": {"type": "string"},
            },
            "required": ["role", "company"],
        },
    },
    {
        "type": "function",
        "name": "checkIndustrySalary",
        "description": "Checks the industry salary range for the given role in the given locatio for the given years of experience",
        "parameters": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "location": {"type": "string"},
                "yearsOfExperience": {"type": "number"},
            },
            "required": ["role", "location", "yearsOfExperience"],
        },
    },
    {
        "type": "function",
        "name": "logFinalOffer",
        "description": "Records the final negotiated terms and outcomes",
        "parameters": {
            "type": "object",
            "properties": {
                "originalOffer": {
                    "type": "object",
                    "properties": {
                        "baseSalary": {"type": "number"},
                        "equity": {"type": "string"},
                        "signOnBonus": {"type": "number"},
                        "title": {"type": "string"},
                    },
                },
                "finalOffer": {
                    "type": "object",
                    "properties": {
                        "baseSalary": {"type": "number"},
                        "equity": {"type": "string"},
                        "signOnBonus": {"type": "number"},
                        "title": {"type": "string"},
                    },
                },
                "nextSteps": {"type": "string"},
            },
            "required": ["originalOffer", "finalOffer", "nextSteps"],
        },
    },
]


def get_tools_for_agent(agent_type: str) -> list:
    """Get the appropriate tools for an agent type."""
    if agent_type == "authentication_agent":
        return AUTHENTICATION_TOOLS
    elif agent_type == "info_desk_agent":
        return INFO_DESK_TOOLS
    elif agent_type == "scheduling_agent":
        return SCHEDULING_TOOLS
    elif agent_type == "negotiation_agent":
        return NEGOTIATION_TOOLS + SCHEDULING_TOOLS
    return []  # main_agent gets no tools by default

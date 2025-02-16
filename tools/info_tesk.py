"""InfoDesk-related tools."""

from typing import Dict, Any
from agents.definitions import ALLOWED_CAREER_FIELDS
import json
from datetime import datetime
from pathlib import Path

# Mock data for each possible field
MOCK_CAREER_DATA = {
    "role": "Senior Software Engineer",
    "experience": "8 years of professional experience",
    "education": "Master's in Computer Science",
    "skills": ["Python", "JavaScript", "AWS", "Docker", "Kubernetes"],
    "availability": "Available to start in 2 weeks",
    "salary_range": "$320,000 - $550,000",
    "location": "San Francisco, CA (Remote friendly)",
    "resume_summary": "Experienced software engineer with focus on cloud architecture and distributed systems",
    "visa_status": "H1B",
    "work_history": [
        {
            "company": "Tech Corp",
            "position": "Senior Software Engineer",
            "duration": "2020-present",
        },
        {
            "company": "Startup Inc",
            "position": "Software Engineer",
            "duration": "2018-2020",
        },
    ],
    "projects": [
        {
            "name": "Cloud Migration",
            "description": "Led migration of legacy systems to AWS",
        },
        {
            "name": "API Platform",
            "description": "Designed and implemented RESTful API platform",
        },
    ],
    "certifications": [
        "AWS Certified Solutions Architect",
        "Google Cloud Professional Engineer",
    ],
}


async def lookupCareerInfo(requestedFields: str) -> Dict[str, Any]:
    """Retrieves requested career information fields.

    Args:
        requestedFields: Comma-separated string of fields to look up

    Returns:
        Dict containing the requested career information fields and their values

    Raises:
        ValueError: If requestedFields is empty or contains invalid fields

    Example:
        requestedFields = "role,experience,skills"
    """
    return MOCK_CAREER_DATA


async def logRecruiterRequest(
    recruiterName: str,
    company: str,
    potentialRole: str,
    potentialRoleDescription: str,
    expectedSalaryRange: str = None,
    expectedLocation: str = None,
    sponsorVisa: bool = None,
    interviewTimeline: str = None,
    interviewProcess: str = None,
) -> None:
    """Logs the recruiter's information request to a text file

    Creates a structured log entry containing all recruiter request details
    in JSON format and appends it to a log file.
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "recruiter_request",
        "recruiter_info": {
            "name": recruiterName,
            "company": company,
        },
        "role_info": {
            "title": potentialRole,
            "description": potentialRoleDescription,
            "salary_range": expectedSalaryRange,
            "location": expectedLocation,
            "visa_sponsorship": sponsorVisa,
            "interview_process": interviewProcess,
            "interview_timeline": interviewTimeline,
        },
    }

    # Ensure the logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Use the current date for the log file name
    log_file = log_dir / f"recruiter_requests_{datetime.now().strftime('%Y-%m-%d')}.txt"

    # Append the log entry to the file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

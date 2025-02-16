import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from config import CURRENT_OFFER_COMPANY
from config import CURRENT_OFFER_ROLE
from config import CURRENT_OFFER_SALARY
from config import CURRENT_OFFER_EQUITY
from config import CURRENT_OFFER_SIGNING_BONUS


async def checkCurrentOffer(company: str, role: str) -> Dict[str, Any]:
    """Checks the details of the current offer."""
    return {
        "company": CURRENT_OFFER_COMPANY,
        "location": "San Francisco",
        "baseSalary": CURRENT_OFFER_SALARY,
        "equity": CURRENT_OFFER_EQUITY,
        "signOnBonus": CURRENT_OFFER_SIGNING_BONUS,
        "title": CURRENT_OFFER_ROLE,
    }


async def checkIndustrySalary(
    role: str, location: str, yearsOfExperience: int
) -> Dict[str, Any]:
    """Checks the industry salary range for the given role in the given location for the given years of experience.

    Args:
        role: The role to check the salary range for
        location: The location to check the salary range for
        yearsOfExperience: Years of experience in the role

    Returns:
        The industry salary range for the given role in the given location for the given years of experience.
    """
    print(
        f"Checking industry salary for {role} in {location} for {yearsOfExperience} years of experience"
    )
    return {
        "salary_min": 200000,
        "salary_max": 500000,
        "salary_average": 350000,
        "currency": "USD",
        "role": role,
        "location": location,
        "yearsOfExperience": yearsOfExperience,
    }


async def logFinalOffer(originalOffer: dict, finalOffer: dict, nextSteps: str) -> None:
    """Records the final negotiated terms and outcomes.

    Args:
        originalOffer: The original offer details including base salary, equity, sign-on bonus, and title
        finalOffer: The final negotiated offer details
        nextSteps: Next steps in the process
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "negotiation_outcome",
        "original_offer": {
            "base_salary": originalOffer["baseSalary"],
            "equity": originalOffer["equity"],
            "sign_on_bonus": originalOffer["signOnBonus"],
            "title": originalOffer["title"],
        },
        "final_offer": {
            "base_salary": finalOffer["baseSalary"],
            "equity": finalOffer["equity"],
            "sign_on_bonus": finalOffer["signOnBonus"],
            "title": finalOffer["title"],
        },
        "improvements": {
            "base_salary_increase": finalOffer["baseSalary"]
            - originalOffer["baseSalary"],
            "sign_on_bonus_increase": finalOffer["signOnBonus"]
            - originalOffer["signOnBonus"],
            "title_change": finalOffer["title"] != originalOffer["title"],
        },
        "next_steps": nextSteps,
    }

    # Ensure the logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Use the current date for the log file name
    log_file = (
        log_dir / f"negotiation_outcomes_{datetime.now().strftime('%Y-%m-%d')}.txt"
    )

    # Append the log entry to the file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False, indent=2) + "\n\n")

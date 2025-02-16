import json
from datetime import datetime
from pathlib import Path


async def checkIndustrySalary(role: str, location: str, yearsOfExperience: int) -> str:
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
    return f"The industry salary range for {role} in {location} for {yearsOfExperience} years of experience is $300,000 - $500,000"


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

async def returnAvailableDateTime(
    suggestedDates: list[str] = None,
    duration: int = 45,
    timeZone: str = "America/Los_Angeles",
) -> list[str]:
    """Returns available dates/times for the next two weeks.

    Args:
        suggestedDates: Optional list of preferred dates from recruiter
        duration: Meeting duration in minutes (default: 45)
        timeZone: Timezone for the meeting (default: America/Los_Angeles)

    Returns:
        List of available datetime strings in ISO format
    """
    if suggestedDates:
        return suggestedDates[0]
    return [
        "2024-03-22T09:00:00-15:00",
        "2024-03-22T10:30:00-13:00",
        "2024-04-05T09:30:00-15:00",
    ]


async def scheduleMeeting(
    dateTime: str,
    duration: int,
    format: str,
    participantName: str,
    participantOrg: str,
    participantEmail: str,
    meetingType: str,
) -> None:
    """Schedules a meeting at the given date and time.

    Args:
        dateTime: Date and time in ISO format
        duration: Meeting duration in minutes
        format: Format of the meeting
        participantName: Meeting participant's name
        participantOrg: Meeting participant's organization (if applicable)
        participantEmail: Meeting participant's email
        meetingType: Type of meeting
    """
    print(
        f"Scheduling {format} {meetingType} meeting between you and {participantName} (email: {participantEmail}) for {dateTime} for {duration} minutes"
    )

"""Main entry point for running the voice services."""

import argparse
import uvicorn
from services.inbound_service import app as inbound_app
from services.outbound_service import app as outbound_app
from config import INBOUND_PORT, OUTBOUND_PORT


def run_inbound_service():
    """Run the inbound voice service."""
    print("Starting inbound voice service...")
    uvicorn.run(inbound_app, host="0.0.0.0", port=INBOUND_PORT)


def run_outbound_service(phone_number: str = None):
    """Run the outbound voice service."""
    print("Starting outbound voice service...")
    if phone_number:
        print(
            "Our recommendation is to always disclose the use of AI for outbound calls.\n"
            "Reminder: All of the rules of TCPA apply even if a call is made by AI.\n"
            "Check with your counsel for legal and compliance advice."
        )
    uvicorn.run(outbound_app, host="0.0.0.0", port=OUTBOUND_PORT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Twilio AI voice services")
    parser.add_argument(
        "--service",
        choices=["inbound", "outbound"],
        required=True,
        help="Which service to run (inbound or outbound)",
    )
    parser.add_argument(
        "--call",
        help="Phone number to call (only for outbound service)",
    )

    args = parser.parse_args()

    if args.service == "inbound":
        if args.call:
            print("Warning: --call argument is ignored for inbound service")
        run_inbound_service()
    else:  # outbound
        run_outbound_service(args.call)

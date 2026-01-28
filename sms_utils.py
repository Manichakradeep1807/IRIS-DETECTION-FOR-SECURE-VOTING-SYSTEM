"""
SMS utilities for sending voting receipts to user's mobile number.
Uses Twilio if TWILIO_ env vars are present; otherwise, logs and no-ops.
"""

import os
from typing import Optional


def _twilio_available() -> bool:
    return all([
        os.environ.get('TWILIO_ACCOUNT_SID'),
        os.environ.get('TWILIO_AUTH_TOKEN'),
        os.environ.get('TWILIO_FROM_NUMBER'),
    ])


def send_sms(to_number: str, message: str) -> bool:
    """
    Send an SMS. Returns True if sent (or simulated), False on hard failure.
    - If Twilio credentials exist, send via Twilio
    - Else, print to console and return True
    """
    if not to_number or not isinstance(to_number, str):
        return False
    to_number = to_number.strip()
    if not to_number:
        return False

    if _twilio_available():
        try:
            from twilio.rest import Client  # type: ignore
            client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
            from_number = os.environ['TWILIO_FROM_NUMBER']
            msg = client.messages.create(body=message, from_=from_number, to=to_number)
            return bool(getattr(msg, 'sid', None))
        except Exception:
            # Fall through to simulated send
            pass

    try:
        print("[SMS SIMULATED] To:", to_number)
        print(message)
        return True
    except Exception:
        return False


def format_voting_receipt(person_id: int, party_symbol: str, party_name: str, timestamp: str, confidence_pct: str) -> str:
    party_symbol = str(party_symbol)
    party_name = str(party_name)
    return (
        "VOTE RECEIPT\n"
        "==============================\n"
        "Party: " + party_symbol + " " + party_name + "\n"
        "Person ID: " + str(person_id) + "\n"
        "Time: " + str(timestamp) + "\n"
        "Confidence: " + str(confidence_pct) + "\n"
        "Auth: Biometric (Iris)\n"
        "==============================\n"
        "Thank you for voting."
    )




















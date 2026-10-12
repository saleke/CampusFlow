import json
import os

FILENAME = "data/tickets.json"


def save_tickets(tickets):
    """F7: Save the master collection of tickets to JSON.

    Raises:
        OSError: If the storage file cannot be written.
    """
    try:
        os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
        with open(FILENAME, 'w') as f:
            json.dump(tickets, f, indent=4)
    except OSError as e:
        raise OSError(f"Could not save tickets to '{FILENAME}': {e}") from e


def _normalize(data):
    """Return the tickets as a dict keyed by ticket ID.

    Accepts the current dict-keyed format as well as a legacy list of tickets
    so older data files still load cleanly.
    """
    if isinstance(data, dict):
        return data

    if isinstance(data, list):
        normalized = {}
        for ticket in data:
            if isinstance(ticket, dict) and ticket.get("id"):
                normalized[ticket["id"]] = ticket
        return normalized

    print(f"\n[CRITICAL ERROR] Storage file '{FILENAME}' has an unsupported structure!")
    print(f"Details: expected an object or list, found {type(data).__name__}.")
    raise SystemExit("Application halted to prevent accidental data erasure.")


def load_tickets():
    """F7: Load tickets from JSON. Handles missing and malformed states cleanly."""
    if not os.path.exists(FILENAME):
        return {}  # Fresh start: dictionary keyed by ticket ID

    try:
        with open(FILENAME, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        # Prevent silent data loss
        print(f"\n[CRITICAL ERROR] Storage file '{FILENAME}' is malformed or corrupted!")
        print(f"Details: {e}")
        raise SystemExit("Application halted to prevent accidental data erasure.")
    except OSError as e:
        print(f"\n[CRITICAL ERROR] Could not read storage file '{FILENAME}'!")
        print(f"Details: {e}")
        raise SystemExit("Application halted to prevent accidental data erasure.")

    return _normalize(data)

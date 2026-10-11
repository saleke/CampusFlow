import json
import os

FILENAME = "data/tickets.json"

def save_tickets(tickets_list):
    """F7: Save the master list of tickets to JSON."""
    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
    with open(FILENAME, 'w') as f:
        json.dump(tickets_list, f, indent=4)

def load_tickets():
    """F7: Load tickets from JSON. Handles missing and malformed states cleanly."""
    if not os.path.exists(FILENAME):
        return []  # Allowed fresh start per prompt guidelines
        
    try:
        with open(FILENAME, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        # Prevent silent data loss
        print(f"\n[CRITICAL ERROR] Storage file '{FILENAME}' is malformed or corrupted!")
        print(f"Details: {e}")
        raise SystemExit("Application halted to prevent accidental data erasure.")

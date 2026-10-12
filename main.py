import sys

from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_prioritized_queue,
    generate_report,
)
# Assuming your partner named their creation module tickets.py
from campusflow.tickets import create_ticket


class _ExitRequested(Exception):
    """Raised when the user ends input (Ctrl-D) or presses Ctrl-C."""


def prompt(text):
    """Read a line of input, converting EOF/interrupt into a clean exit."""
    try:
        return input(text)
    except (EOFError, KeyboardInterrupt) as e:
        raise _ExitRequested() from e


def _fmt(ticket, field, default="N/A"):
    value = ticket.get(field, default)
    return default if value is None else value


def handle_choice(choice, tickets):
    """Handle one menu selection. Returns False when the user wants to exit."""
    if choice == "1":
        title = prompt("Enter ticket title: ")
        category = prompt("Enter category (Network, Hardware, Software, Other): ")
        urgency = prompt("Enter urgency (low, medium, high): ")
        users = prompt("Enter number of affected users: ")
        try:
            input_data = {
                "title": title,
                "category": category,
                "urgency": urgency,
                "affected_users": users,
            }
            new_ticket = create_ticket(input_data, tickets)
        except ValueError as e:
            print(f"[ERROR] Failed to create ticket: {e}")
            return True

        try:
            save_tickets(tickets)
        except OSError as e:
            print(f"[ERROR] Ticket {new_ticket['id']} created but could not be saved: {e}")
            return True

        print(f"[SUCCESS] Ticket created with ID: {new_ticket['id']} and Priority: {new_ticket['priority']}")

    elif choice == "2":
        if not tickets:
            print("No tickets found.")
            return True

        sub_choice = prompt("Type 'ALL' to view all or enter a specific Ticket ID (e.g., T001): ").strip().upper()

        if sub_choice == "ALL":
            for t in tickets.values():
                print(f"[{_fmt(t, 'id')}] {_fmt(t, 'title')} | Status: {_fmt(t, 'status')} | Priority: {_fmt(t, 'priority')} | Assigned To: {_fmt(t, 'assigned_to')}")
        else:
            match = tickets.get(sub_choice)
            if match is None:
                print("[ERROR] Ticket ID not found.")
            else:
                print(f"\nID: {_fmt(match, 'id')}")
                print(f"Title: {_fmt(match, 'title')}")
                print(f"Category: {_fmt(match, 'category')}")
                print(f"Urgency: {_fmt(match, 'urgency')}")
                print(f"Affected Users: {_fmt(match, 'affected_users')}")
                print(f"Priority: {_fmt(match, 'priority')}")
                print(f"Status: {_fmt(match, 'status')}")
                print(f"Assigned To: {_fmt(match, 'assigned_to')}")

    elif choice == "3":
        t_id = prompt("Enter Ticket ID to assign: ").strip().upper()
        name = prompt("Enter staff member's name: ").strip()
        try:
            assign_ticket(tickets, t_id, name)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return True

        try:
            save_tickets(tickets)
        except OSError as e:
            print(f"[ERROR] Ticket {t_id} assigned but could not be saved: {e}")
            return True

        print(f"[SUCCESS] Ticket {t_id} assigned to {name}.")

    elif choice == "4":
        t_id = prompt("Enter Ticket ID to update: ").strip().upper()
        match = tickets.get(t_id)
        if match is None:
            print("[ERROR] Ticket ID not found.")
            return True

        new_status = prompt("Enter new status (open, in_progress, resolved): ").strip().lower()
        try:
            update_status(match, new_status)
        except ValueError as e:
            print(f"[ERROR] {e}")
            return True

        try:
            save_tickets(tickets)
        except OSError as e:
            print(f"[ERROR] Status updated but could not be saved: {e}")
            return True

        print(f"[SUCCESS] Ticket {t_id} status updated to '{new_status}'.")

    elif choice == "5":
        queue = get_prioritized_queue(tickets)
        print("\n--- PRIORITIZED WORK QUEUE ---")
        if not queue:
            print("No open, unresolved tickets.")
        for t in queue:
            print(f"[{str(_fmt(t, 'priority', 'unknown')).upper()}] {_fmt(t, 'id')}: {_fmt(t, 'title')} (Status: {_fmt(t, 'status')})")

    elif choice == "6":
        rep = generate_report(tickets)
        print(f"\n--- CAMPUSFLOW REPORT ---")
        print(f"Total Tickets Logged: {rep['total']}")
        print(f"Status Breakdowns: {rep['status']}")
        print(f"Priority Breakdowns: {rep['priority']}")

    elif choice == "7":
        print("Exiting CampusFlow. Goodbye!")
        return False

    else:
        print("Invalid selection. Try again.")

    return True


def main():
    print("Welcome to CampusFlow Helpdesk Manager")

    # F7: Load on startup
    try:
        tickets = load_tickets()
    except SystemExit:
        sys.exit(1)

    try:
        while True:
            print("\n=== CAMPUSFLOW MENU ===")
            print("1. Create Ticket (F1)")
            print("2. View All / Single Ticket (F2)")
            print("3. Assign Ticket (F3)")
            print("4. Update Workflow Status (F4)")
            print("5. View Prioritized Work Queue (F5)")
            print("6. Generate Metrics Report (F6)")
            print("7. Exit")

            choice = prompt("Select an option (1-7): ").strip()

            try:
                if not handle_choice(choice, tickets):
                    break
            except _ExitRequested:
                raise
            except Exception as e:
                # Never crash the CLI: report the failure and return to the menu.
                print(f"[ERROR] Unexpected failure: {e}")
    except _ExitRequested:
        print("\nExiting CampusFlow. Goodbye!")


if __name__ == "__main__":
    main()

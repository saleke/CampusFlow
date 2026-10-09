import sys
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import assign_ticket, update_status, get_prioritized_queue, generate_report
# Assuming your partner named their creation module tickets.py
from campusflow.tickets import create_ticket 

def main():
    print("Welcome to CampusFlow Helpdesk Manager")
    
    # F7: Load on startup
    try:
        tickets = load_tickets()
    except SystemExit:
        sys.exit(1)

    while True:
        print("\n=== CAMPUSFLOW MENU ===")
        print("1. Create Ticket (F1)")
        print("2. View All / Single Ticket (F2)")
        print("3. Assign Ticket (F3)")
        print("4. Update Workflow Status (F4)")
        print("5. View Prioritized Work Queue (F5)")
        print("6. Generate Metrics Report (F6)")
        print("7. Exit")
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == "1":
            title = input("Enter ticket title: ")
            category = input("Enter category (Network, Hardware, Software, Other): ")
            urgency = input("Enter urgency (low, medium, high): ")
            try:
                users = int(input("Enter number of affected users: "))
                # Call Engineer A's creation function
                new_ticket = create_ticket(tickets, title, category, urgency, users)
                save_tickets(tickets)  # Persist changes
                print(f"[SUCCESS] Ticket created with ID: {new_ticket['id']} and Priority: {new_ticket['priority']}")
            except Exception as e:
                print(f"[ERROR] Failed to create ticket: {e}")
                
        elif choice == "2":
            if not tickets:
                print("No tickets found.")
                continue
            sub_choice = input("Type 'ALL' to view all or enter a specific Ticket ID (e.g., T001): ").strip().upper()
            if sub_choice == "ALL":
                for t in tickets:
                    print(f"[{t['id']}] {t['title']} | Status: {t['status']} | Priority: {t['priority']} | Assigned To: {t['assigned_to']}")
            else:
                match = next((t for t in tickets if t["id"] == sub_choice), None)
                if match:
                    print(f"\nID: {match['id']}\nTitle: {match['title']}\nCategory: {match['category']}\nUrgency: {match['urgency']}\nAffected Users: {match['affected_users']}\nPriority: {match['priority']}\nStatus: {match['status']}\nAssigned To: {match['assigned_to']}")
                else:
                    print("[ERROR] Ticket ID not found.")

        elif choice == "3":
            t_id = input("Enter Ticket ID to assign: ").strip().upper()
            name = input("Enter staff member's name: ").strip()
            try:
                assign_ticket(tickets, t_id, name)
                save_tickets(tickets)
                print(f"[SUCCESS] Ticket {t_id} assigned to {name}.")
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif choice == "4":
            t_id = input("Enter Ticket ID to update: ").strip().upper()
            match = next((t for t in tickets if t["id"] == t_id), None)
            if not match:
                print("[ERROR] Ticket ID not found.")
                continue
            new_status = input("Enter new status (open, in_progress, resolved): ").strip().lower()
            try:
                update_status(match, new_status)
                save_tickets(tickets)
                print(f"[SUCCESS] Ticket {t_id} status updated to '{new_status}'.")
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif choice == "5":
            queue = get_prioritized_queue(tickets)
            print("\n--- PRIORITIZED WORK QUEUE ---")
            if not queue:
                print("No open, unresolved tickets.")
            for t in queue:
                print(f"[{t['priority'].upper()}] {t['id']}: {t['title']} (Status: {t['status']})")

        elif choice == "6":
            rep = generate_report(tickets)
            print(f"\n--- CAMPUSFLOW REPORT ---")
            print(f"Total Tickets Logged: {rep['total']}")
            print(f"Status Breakdowns: {rep['status']}")
            print(f"Priority Breakdowns: {rep['priority']}")

        elif choice == "7":
            print("Exiting CampusFlow. Goodbye!")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()

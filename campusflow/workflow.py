def assign_ticket(tickets_list, ticket_id, staff_name):
    """F3: Assign a ticket to a staff member."""
    if not staff_name or str(staff_name).strip() == "":
        raise ValueError("Staff name cannot be empty.")
        
    for ticket in tickets_list:
        if ticket["id"] == ticket_id:
            ticket["assigned_to"] = staff_name.strip()
            return True
            
    raise ValueError(f"Ticket ID {ticket_id} not found.")

def update_status(ticket, new_status):
    """F4: Workflow state machine adjustments."""
    current = ticket["status"]
    
    # Validation Rules
    if current == "resolved" and new_status != "open":
        raise ValueError("Resolved tickets must be explicitly reopened to 'open' first.")
    if new_status == "in_progress" and ticket["assigned_to"] is None:
        raise ValueError("Cannot move an unassigned ticket to in_progress.")
        
    # Enforce strict sequential transitions
    if current == "open" and new_status not in ["in_progress", "resolved"]:
        raise ValueError("From 'open', ticket can only go to 'in_progress' or 'resolved'.")
    if current == "in_progress" and new_status != "resolved":
        raise ValueError("From 'in_progress', ticket can only go to 'resolved'.")
        
    ticket["status"] = new_status
    return True

def get_prioritized_queue(tickets_list):
    """F5: Work queue sorted by critical -> high -> medium -> low, then by ID."""
    priority_order = {"critical": 1, "high": 2, "medium": 3, "low": 4}
    
    # Whitelist unresolved statuses
    unresolved = [t for t in tickets_list if t["status"] in ["open", "in_progress"]]
    
    # Multi-criteria sort
    return sorted(unresolved, key=lambda t: (priority_order.get(t["priority"], 5), t["id"]))

def generate_report(tickets_list):
    """F6: Calculate breakdowns by status and priority."""
    report = {
        "total": len(tickets_list),
        "status": {"open": 0, "in_progress": 0, "resolved": 0},
        "priority": {"critical": 0, "high": 0, "medium": 0, "low": 0}
    }
    
    for t in tickets_list:
        if t["status"] in report["status"]:
            report["status"][t["status"]] += 1
        if t["priority"] in report["priority"]:
            report["priority"][t["priority"]] += 1
            
    return report

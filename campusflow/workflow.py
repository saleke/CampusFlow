"""Workflow lifecycle operations for CampusFlow (F3-F6).

Engineer A stores the master collection as a dictionary keyed by ticket ID,
while Engineer B's original workflow code (and its unit tests) operate on a
plain list of tickets.  To let the two halves merge without breaking either
side, every public function here accepts *either* shape:

* a mapping keyed by ticket ID (``{"T001": {...}}``), or
* an iterable of ticket dictionaries (``[{...}, {...}]``).
"""

from collections.abc import Mapping

VALID_STATUSES = ("open", "in_progress", "resolved")


def _ticket_values(tickets):
    """Return the ticket dictionaries from either a mapping or an iterable."""
    if isinstance(tickets, Mapping):
        return list(tickets.values())
    return list(tickets)


def _find_ticket(tickets, ticket_id):
    """Return the ticket whose ``id`` matches ``ticket_id``, or ``None``.

    Supports a mapping keyed by ticket ID as well as a list of tickets, and
    tolerates a mapping whose keys do not match the ``id`` field.
    """
    if isinstance(tickets, Mapping):
        candidate = tickets.get(ticket_id)
        if isinstance(candidate, Mapping) and candidate.get("id") == ticket_id:
            return candidate

    for ticket in _ticket_values(tickets):
        if isinstance(ticket, Mapping) and ticket.get("id") == ticket_id:
            return ticket

    return None


def assign_ticket(tickets, ticket_id, staff_name):
    """F3: Assign a ticket to a staff member.

    Raises:
        ValueError: If the staff name is blank or the ticket ID is unknown.
    """
    if not staff_name or str(staff_name).strip() == "":
        raise ValueError("Staff name cannot be empty.")

    ticket = _find_ticket(tickets, ticket_id)
    if ticket is None:
        raise ValueError(f"Ticket ID {ticket_id} not found.")

    ticket["assigned_to"] = staff_name.strip()
    return True


def update_status(ticket, new_status):
    """F4: Workflow state machine adjustments.

    Raises:
        ValueError: If the ticket is malformed or the transition is invalid.
    """
    if new_status not in VALID_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")

    current = ticket.get("status") if isinstance(ticket, Mapping) else None
    if current is None:
        raise ValueError("Ticket is missing a valid 'status' field.")

    # Validation Rules
    if current == "resolved" and new_status != "open":
        raise ValueError("Resolved tickets must be explicitly reopened to 'open' first.")
    if new_status == "in_progress" and ticket.get("assigned_to") is None:
        raise ValueError("Cannot move an unassigned ticket to in_progress.")

    # Enforce strict sequential transitions
    if current == "open" and new_status not in ["in_progress", "resolved"]:
        raise ValueError("From 'open', ticket can only go to 'in_progress' or 'resolved'.")
    if current == "in_progress" and new_status != "resolved":
        raise ValueError("From 'in_progress', ticket can only go to 'resolved'.")

    ticket["status"] = new_status
    return True


def get_prioritized_queue(tickets):
    """F5: Work queue sorted by critical -> high -> medium -> low, then by ID."""
    priority_order = {"critical": 1, "high": 2, "medium": 3, "low": 4}

    # Whitelist unresolved statuses
    unresolved = [
        t for t in _ticket_values(tickets)
        if t.get("status") in ["open", "in_progress"]
    ]

    # Multi-criteria sort
    return sorted(
        unresolved,
        key=lambda t: (priority_order.get(t.get("priority"), 5), t.get("id")),
    )


def generate_report(tickets):
    """F6: Calculate breakdowns by status and priority."""
    values = _ticket_values(tickets)
    report = {
        "total": len(values),
        "status": {"open": 0, "in_progress": 0, "resolved": 0},
        "priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
    }

    for t in values:
        status = t.get("status")
        if status in report["status"]:
            report["status"][status] += 1
        priority = t.get("priority")
        if priority in report["priority"]:
            report["priority"][priority] += 1

    return report

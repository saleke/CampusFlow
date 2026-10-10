"""Ticket validation, priority calculation, and creation for CampusFlow."""

from collections.abc import Mapping, MutableMapping
from typing import Any


CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

URGENCIES = {"low", "medium", "high"}

TICKET_FIELDS = {
    "id",
    "title",
    "category",
    "urgency",
    "affected_users",
    "priority",
    "status",
    "assigned_to",
}


def validate_ticket_data(
    title: Any,
    category: Any,
    urgency: Any,
    affected_users: Any,
) -> dict[str, Any]:
    """Validate ticket inputs and return normalized values.

    Raises:
        ValueError: If any value is invalid.
    """
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")
    normalized_title = title.strip()

    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    normalized_category = CATEGORIES.get(category.strip().casefold())
    if normalized_category is None:
        raise ValueError("Invalid category. Choose Network, Hardware, Software, or Other.")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")
    normalized_urgency = urgency.strip().casefold()
    if normalized_urgency not in URGENCIES:
        raise ValueError("Invalid urgency. Choose low, medium, or high.")

    # bool is a subclass of int in Python, so reject it explicitly.
    if isinstance(affected_users, bool):
        raise ValueError("Affected users must be a positive whole number.")

    if isinstance(affected_users, str):
        raw_count = affected_users.strip()
        # int() accepts signs such as +3, but rejects decimals such as 3.0.
        try:
            normalized_users = int(raw_count)
        except ValueError as exc:
            raise ValueError("Affected users must be a positive whole number.") from exc
    elif isinstance(affected_users, int):
        normalized_users = affected_users
    else:
        raise ValueError("Affected users must be a positive whole number.")

    if normalized_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return {
        "title": normalized_title,
        "category": normalized_category,
        "urgency": normalized_urgency,
        "affected_users": normalized_users,
    }


def calculate_priority(urgency: str, affected_users: int) -> str:
    """Return priority according to CampusFlow's rules."""

    # 1. Check the type before checking set membership.
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")

    # 2. Check that the urgency is allowed.
    urgency = urgency.strip().lower()
    if urgency not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    # 3. Validate the number of affected users.
    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a positive whole number.")
    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    # 4. Apply priority rules in the correct order.
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def _next_ticket_id(tickets):
    highest_number = 0

    for ticket_id in tickets:
        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            number = int(ticket_id[1:])

            if number > highest_number:
                highest_number = number

    return f"T{highest_number + 1:03d}"



def create_ticket(
    ticket_data: Mapping[str, Any],
    tickets: MutableMapping[str, dict[str, Any]],
) -> dict[str, Any]:
    """Validate, build, and store a ticket; return the created ticket.

    The shared collection is modified only after all input validation succeeds.
    """
    if not isinstance(ticket_data, Mapping):
        raise ValueError("Ticket data must be a mapping of field names to values.")

    required_fields = {"title", "category", "urgency", "affected_users"}
    missing_fields = required_fields - ticket_data.keys()
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Missing required ticket field(s): {missing}")

    validated = validate_ticket_data(
        title=ticket_data["title"],
        category=ticket_data["category"],
        urgency=ticket_data["urgency"],
        affected_users=ticket_data["affected_users"],
    )
    priority = calculate_priority(
        validated["urgency"],
        validated["affected_users"],
    )

    ticket_id = _next_ticket_id(tickets)
    ticket = {
        "id": ticket_id,
        **validated,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }

    # Commit only after the ticket is fully validated and constructed.
    tickets[ticket_id] = ticket
    return ticket
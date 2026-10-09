# Design Decisions - CampusFlow

## 1. Responsibilities
* **Engineer A (Name):** Ticket creation, input validation, priority engine, and matching tests.
* **Engineer B (Name):** Assignment, lifecycle, queue, reports, and matching tests.
* **Shared:** JSON storage and CLI menu integration.

## 2. Core Data Structure
A single ticket will be represented as a standard Python dictionary:
{
  "id": "T001",
  "title": "...",
  "category": "...",
  "urgency": "...",
  "affected_users": 1,
  "priority": "...",
  "status": "open",
  "assigned_to": None
}
All tickets will live inside a master **list of dictionaries** `[]`.

## 3. Function Contracts (How our modules interact)
* `create_ticket(tickets_list, title, category, urgency, affected_users) -> dict`
  * Raises `ValueError` if input validation fails.
* `calculate_priority(urgency, affected_users) -> str`
  * Returns: 'critical', 'high', 'medium', or 'low'.
* `assign_ticket(tickets_list, ticket_id, staff_name) -> bool`
  * Returns `True` if successful, raises `ValueError` if ID doesn't exist.
* `update_status(tickets_list, ticket_id, new_status) -> bool`
  * Enforces state machine transitions.

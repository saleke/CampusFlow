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





### Engineer B

### Interaction 1: Ticket Queue Filtering & Sorting
* **AI Suggestion:** Use `t["status"] != "resolved"` to find unresolved tickets.
* **My Correction/Improvement:** I rejected the negative check and changed it to an explicit whitelist `t["status"] in ["open", "in_progress"]`. This prevents the system from accidentally pulling in invalid or future statuses, keeping our workflow strictly bound to F4 and F5.

### Interaction 2: Workflow State Transitions
* **AI Suggestion:** A basic validation function checking isolated rules.
* **My Correction/Improvement:** I pointed out that it allowed skipping states (e.g., jumping from `open` to `resolved`). I redesigned it to enforce sequential valid moves (`open` ➔ `in_progress` ➔ `resolved`) based on the current state.


### Interaction 3: JSON Persistence Error Handling
* **AI Suggestion:** Use a generic `except Exception:` block inside `load_tickets()` that falls back to returning an empty list `[]`.
* **My Correction/Improvement:** I rejected this approach because it would silently overwrite and erase corrupted files. I modified it to catch `json.JSONDecodeError` explicitly, allowing the application to raise a clear error to protect student ticket data.

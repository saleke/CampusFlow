# Design Decisions - CampusFlow

## 1. Responsibilities
### Engineer A — Ticket Creation and Priority Engine

**Implementation decision**

I chose to store tickets in a dictionary using the ticket ID as the key. Each ticket contains its title, category, urgency, number of affected users, calculated priority, status, and assigned staff member. This makes it straightforward to retrieve a ticket by its unique ID.

I also separated input validation from priority calculation so that invalid data is rejected before a ticket is added to the collection.

**Relevant test**
I tested that creating a ticket with invalid data does not modify the ticket collection. This verifies that the system rejects invalid input without leaving an incomplete ticket behind.

**What I learned**
I learned the importance of validating data before changing the system's state and testing both successful and unsuccessful operations.


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
All tickets live inside a master **dictionary keyed by ticket ID** `{"T001": {...}}`.
This makes lookups by ID O(1) and is the format written to `data/tickets.json`.

> Merge note: Engineer B's workflow functions originally assumed a list of
> tickets. To merge both halves safely, the workflow functions now accept
> **either** the dictionary-keyed collection **or** a plain list. Legacy JSON
> files stored as a list are normalized to the dictionary format on load.

## 3. Function Contracts (How our modules interact)
* `create_ticket(ticket_data, tickets) -> dict`
  * `ticket_data` is a mapping with `title`, `category`, `urgency`, and `affected_users`.
  * Raises `ValueError` if input validation fails; only mutates `tickets` on success.
* `calculate_priority(urgency, affected_users) -> str`
  * Returns: 'critical', 'high', 'medium', or 'low'.
* `assign_ticket(tickets, ticket_id, staff_name) -> bool`
  * Returns `True` if successful, raises `ValueError` if the ID doesn't exist.
* `update_status(ticket, new_status) -> bool`
  * Enforces state machine transitions and raises `ValueError` on invalid moves.


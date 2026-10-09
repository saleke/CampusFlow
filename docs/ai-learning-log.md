


# ENGINEER B

### Interaction 1: Ticket Queue Filtering & Sorting
* **AI Suggestion:** Use `t["status"] != "resolved"` to find unresolved tickets.
* **My Correction/Improvement:** I rejected the negative check and changed it to an explicit whitelist `t["status"] in ["open", "in_progress"]`. This prevents the system from accidentally pulling in invalid or future statuses, keeping our workflow strictly bound to F4 and F5.

### Interaction 2: Workflow State Transitions
* **AI Suggestion:** A basic validation function checking isolated rules.
* **My Correction/Improvement:** I pointed out that it allowed skipping states (e.g., jumping from `open` to `resolved`). I redesigned it to enforce sequential valid moves (`open` ➔ `in_progress` ➔ `resolved`) based on the current state.

### Interaction 3: JSON Persistence Error Handling
* **AI Suggestion:** Use a generic `except Exception:` block inside `load_tickets()` that falls back to returning an empty list `[]`.
* **My Correction/Improvement:** I rejected this approach because it would silently overwrite and erase corrupted files. I modified it to catch `json.JSONDecodeError` explicitly, allowing the application to raise a clear error to protect student ticket data.

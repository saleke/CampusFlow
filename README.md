# CampusFlow Helpdesk Manager

CampusFlow is a Python command-line technical support ticket manager built for the Learn2Earn campus staff. The application records technical problems, validates user inputs, automatically calculates ticket priorities based on operational urgency, and provides an optimized workflow for ticket assignment, queue management, and metrics reporting.

---

## Team Contributions and Roles

This project was built collaboratively by a two-person engineering team within a six-hour sprint checkpoint.

### Engineer A
* **Ownership Areas:** Ticket creation (F1), input validation, automatic priority calculation engine, and creation unit tests.

### Engineer B
* **Ownership Areas:** Ticket assignment (F3), workflow state machine (F4), prioritized work queue management (F5), metrics reports (F6), JSON file persistence (F7), and workflow lifecycle unit tests.

---

## Project Structure

```text
campusflow/
├── README.md
├── .gitignore
├── main.py
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   └── storage.py
├── tests/
│   ├── test_tickets.py
│   └── test_workflow.py
└── docs/
    ├── ai-learning-log.md
    └── design-decisions.md
```

---

## Technical Features

### F1: Create Ticket
Collects details including title, category, urgency, and affected users. Inputs are validated before saving to prevent invalid data states.

### F2: List and View
Allows administrators to output all active tickets simultaneously or query a single ticket record using its unique identifier.

### F3: Assign Ticket
Assigns responsible staff members to open tickets while rejecting empty names or invalid ticket tracking identifiers.

### F4: Workflow State Machine
Enforces sequential transitions from open to in_progress to resolved. It explicitly blocks unassigned tickets from entering progress and requires an explicit reopen command to modify resolved records.

### F5: Prioritized Work Queue
Displays unresolved items sorted systematically by priority level (critical, high, medium, low). Ties are broken chronologically using the earlier numeric ticket ID.

### F6: Metrics Reports
Generates business intelligence metrics including total ticket volume, current status breakdowns, and priority distributions.

### F7: JSON Persistence
Saves all data to an external file structure and loads records on startup. Includes robust data defenses to halt the program if a file is malformed rather than silently destroying user data.

---

## Requirements and Setup

### Prerequisites
* Python 3.8 or higher
* Standard standard library modules (json, os, unittest, sys)

### Installation
1. Clone the repository to your local machine:
   ```bash
   git clone <your-repository-url>
   cd campusflow-team
   ```

2. Run the application directly from the root directory:
   ```bash
   python3 main.py
   ```

---

## Running Automated Tests

A comprehensive suite of automated unit tests protects the integrity of the business logic. To execute all test modules simultaneously, run the discovery tool from the root directory:

```bash
python3 -m unittest discover -s tests
```

---

## Development Metrics and Validation

* **Validation Rules:** All user entries are normalized. Text inputs are stripped of trailing spaces, and integers are checked to ensure they are positive values.
* **Data Defense:** The JSON system uses explicit exception blocks for decoding errors to safeguard historical logs from being replaced by empty structures.

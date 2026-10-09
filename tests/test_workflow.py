import unittest
from campusflow.workflow import assign_ticket, update_status, get_prioritized_queue, generate_report

class TestWorkflowAndLifecycle(unittest.TestCase):

    def setUp(self):
        """Set up a fresh mock ticket list before every individual test run."""
        self.tickets = [
            {"id": "T001", "title": "Wi-Fi down", "category": "Network", "urgency": "high", "affected_users": 15, "priority": "critical", "status": "open", "assigned_to": None},
            {"id": "T002", "title": "Broken mouse", "category": "Hardware", "urgency": "low", "affected_users": 1, "priority": "low", "status": "open", "assigned_to": "Alice"},
            {"id": "T003", "title": "Software crash", "category": "Software", "urgency": "medium", "affected_users": 5, "priority": "medium", "status": "in_progress", "assigned_to": "Bob"}
        ]

    # --- F3: ASSIGNMENT TESTS ---
    def test_assign_ticket_success(self):
        """Verify ticket can be successfully assigned to a staff member."""
        result = assign_ticket(self.tickets, "T001", "Charlie")
        self.assertTrue(result)
        self.assertEqual(self.tickets[0]["assigned_to"], "Charlie")

    def test_assign_ticket_invalid_id_raises_error(self):
        """Verify assigning an invalid ticket ID raises a ValueError."""
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Charlie")

    def test_assign_ticket_empty_name_raises_error(self):
        """Verify assigning to an empty staff name raises a ValueError."""
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    # --- F4: WORKFLOW STATE MACHINE TESTS ---
    def test_workflow_unassigned_cannot_start(self):
        """Verify an unassigned ticket CANNOT move to in_progress."""
        with self.assertRaises(ValueError):
            update_status(self.tickets[0], "in_progress")

    def test_workflow_sequential_transition_success(self):
        """Verify valid state updates transition correctly."""
        # T002 is assigned to Alice and open, moving to in_progress should work
        self.assertTrue(update_status(self.tickets[1], "in_progress"))
        self.assertEqual(self.tickets[1]["status"], "in_progress")

    def test_workflow_resolved_must_reopen_first(self):
        """Verify a resolved ticket rejects modification unless explicitly reopened."""
        ticket = {"id": "T004", "status": "resolved", "assigned_to": "Alice", "priority": "low"}
        with self.assertRaises(ValueError):
            update_status(ticket, "in_progress")

    # --- F5: WORK QUEUE SORTING TESTS ---
    def test_queue_sorting_and_filtering(self):
        """Verify queue filters resolved items and sorts correctly (Priority then ID)."""
        # Add a resolved ticket that should be ignored
        self.tickets.append({"id": "T000", "priority": "critical", "status": "resolved", "assigned_to": "Dave"})
        
        queue = get_prioritized_queue(self.tickets)
        
        # T000 should be omitted. T001 (critical) must be first, followed by T003 (medium), then T002 (low)
        self.assertEqual(len(queue), 3)
        self.assertEqual(queue[0]["id"], "T001")
        self.assertEqual(queue[1]["id"], "T003")
        self.assertEqual(queue[2]["id"], "T002")

    # --- F6: REPORTING TESTS ---
    def test_generate_report_metrics(self):
        """Verify reports calculate correct breakdown configurations."""
        report = generate_report(self.tickets)
        self.assertEqual(report["total"], 3)
        self.assertEqual(report["status"]["open"], 2)
        self.assertEqual(report["status"]["in_progress"], 1)
        self.assertEqual(report["priority"]["critical"], 1)

if __name__ == '__main__':
    unittest.main()

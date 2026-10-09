"""Automated tests for CampusFlow ticket validation and creation."""

import unittest

from campusflow.tickets import calculate_priority, create_ticket, validate_ticket_data


class TestValidateTicketData(unittest.TestCase):
    def test_valid_data_is_normalized(self):
        result = validate_ticket_data(
            "  Wi-Fi is down  ", " NETWORK ", " HIGH ", "3"
        )
        self.assertEqual(
            result,
            {
                "title": "Wi-Fi is down",
                "category": "Network",
                "urgency": "high",
                "affected_users": 3,
            },
        )

    def test_blank_title_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Title must not be blank"):
            validate_ticket_data("   ", "Network", "low", 1)

    def test_invalid_category_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid category"):
            validate_ticket_data("Printer issue", "Facilities", "low", 1)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid urgency"):
            validate_ticket_data("Printer issue", "Hardware", "urgent", 1)

    def test_affected_users_must_be_positive_whole_number(self):
        for value in (0, -1, "3.5", "abc", True, 2.5):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_ticket_data("Printer issue", "Hardware", "low", value)


class TestCalculatePriority(unittest.TestCase):
    def test_priority_rules_and_boundaries(self):
        cases = [
            ("high", 10, "critical"),
            ("high", 2, "high"),
            ("low", 10, "high"),
            ("medium", 1, "medium"),
            ("low", 3, "medium"),
            ("low", 2, "low"),
            ("medium", 10, "high"),
        ]
        for urgency, users, expected in cases:
            with self.subTest(urgency=urgency, users=users):
                self.assertEqual(calculate_priority(urgency, users), expected)

    def test_invalid_priority_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", 3)
        with self.assertRaises(ValueError):
            calculate_priority("low", True)
        with self.assertRaises(ValueError):
            calculate_priority("low", 0)
    
    def test_non_string_urgency_is_rejected(self):
        for urgency in (["high"], None, 123):
            with self.subTest(urgency=urgency):
                with self.assertRaises(ValueError):
                    calculate_priority(urgency, 12)



class TestCreateTicket(unittest.TestCase):
    def setUp(self):
        self.tickets = {}

    def test_create_ticket_has_all_required_fields_and_defaults(self):
        ticket = create_ticket(
            {
                "title": "Campus Wi-Fi is unavailable",
                "category": "Network",
                "urgency": "high",
                "affected_users": 12,
            },
            self.tickets,
        )
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertEqual(
            set(ticket),
            {
                "id", "title", "category", "urgency", "affected_users",
                "priority", "status", "assigned_to",
            },
        )
        self.assertIs(self.tickets["T001"], ticket)

    def test_ids_are_unique_and_fill_first_gap(self):
        self.tickets.update({
            "T001": {"id": "T001"},
            "T003": {"id": "T003"},
        })
        ticket = create_ticket(
            {
                "title": "Keyboard failure",
                "category": "Hardware",
                "urgency": "low",
                "affected_users": 1,
            },
            self.tickets,
        )
        self.assertEqual(ticket["id"], "T002")

    def test_invalid_creation_does_not_change_collection(self):
        before = dict(self.tickets)
        with self.assertRaises(ValueError):
            create_ticket(
                {
                    "title": "   ",
                    "category": "Network",
                    "urgency": "low",
                    "affected_users": 1,
                },
                self.tickets,
            )
        self.assertEqual(self.tickets, before)

    def test_missing_fields_are_reported(self):
        with self.assertRaisesRegex(ValueError, "Missing required"):
            create_ticket({"title": "Wi-Fi issue"}, self.tickets)
        self.assertEqual(self.tickets, {})



if __name__ == "__main__":
    unittest.main()
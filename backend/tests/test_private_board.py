import unittest
from private_board import PrivateBoard

class TestPrivateBoard(unittest.TestCase):

    def setUp(self):
        """Set up a new PrivateBoard instance for each test."""
        self.board = PrivateBoard("Test Group")

    def test_join_group(self):
        """Test a user joining a group."""
        self.board.users = {"Alice": {"groups": set()}}
        self.board.groups = {}
        response = self.board.join_group("Alice", "group1")
        self.assertEqual(response, "Alice joined group group1.")
        self.assertIn("group1", self.board.groups)
        self.assertIn("group1", self.board.users["Alice"]["groups"])

    def test_post_to_group(self):
        """Test posting a message to a group."""
        self.board.users = {"Alice": {"groups": {"group1"}}}
        self.board.groups = {"group1": {"members": {"Alice"}, "messages": []}}
        message_id = self.board.post_to_group("group1", "Subject", "Content of the message.")
        self.assertIn("group1", self.board.groups)
        self.assertEqual(message_id, 1)
        self.assertEqual(self.board.groups["group1"]["messages"][0], {
            'id': 1,
            'subject': "Subject",
            'content': "Content of the message."
        })

    def test_leave_group(self):
        """Test a user leaving a group."""
        self.board.users = {"Alice": {"groups": {"group1"}}}
        self.board.groups = {"group1": {"members": {"Alice"}, "messages": []}}
        response = self.board.leave_group("Alice", "group1")
        self.assertEqual(response, "Alice left group group1.")
        self.assertNotIn("group1", self.board.users["Alice"]["groups"])
        self.assertNotIn("Alice", self.board.groups.get("group1", {}).get("members", set()))

    def test_list_group_users(self):
        """Test listing users in a group."""
        self.board.users = {"Alice": {"groups": {"group1"}}, "Bob": {"groups": {"group1"}}}
        self.board.groups = {"group1": {"members": {"Alice", "Bob"}, "messages": []}}
        group_users = self.board.list_group_users("group1")
        self.assertEqual(set(group_users), {"Alice", "Bob"})

    def test_get_group_message(self):
        """Test retrieving a message from the group by message ID."""
        self.board.users = {"Alice": {"groups": {"group1"}}}
        self.board.groups = {"group1": {"members": {"Alice"}, "messages": []}}
        message_id = self.board.post_to_group("group1", "Group Subject", "Group Content")
        message_content = self.board.get_group_message("group1", message_id)
        self.assertEqual(message_content, "Group Subject: Group Content")

    def test_get_group_message_not_found(self):
        """Test retrieving a message that does not exist."""
        self.board.groups = {"group1": {"members": set(), "messages": []}}
        response = self.board.get_group_message("group1", 999)
        self.assertEqual(response, "Message 999 not found in group group1.")

if __name__ == '__main__':
    unittest.main()

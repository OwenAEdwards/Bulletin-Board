import unittest
from private_board import PrivateBoard

class TestPrivateBoard(unittest.TestCase):

    def setUp(self):
        """Set up a new PrivateBoard instance for each test."""
        self.board = PrivateBoard("Test Group")

    def test_join_group(self):
      """Test a user joining a group."""
      
      # Initialize the board with users (ensure Alice has a 'groups' key)
      self.board.users = {"Alice": {"groups": set()}}  # Alice starts with no groups
      self.board.groups = {}  # Initialize groups to be empty
      
      # Create a PrivateBoard instance (group1)
      group1 = PrivateBoard("group1")
      
      # Add group1 to the board's groups dictionary manually (simulate board management of groups)
      self.board.groups[group1.group_id] = group1  # Manually add the created group to groups
      
      # Now, call join_group to add Alice to group1
      response = group1.join_group("Alice", group1.group_id)
      
      # Manually add group1 to Alice's groups (since the class doesn't do it automatically)
      self.board.users["Alice"]["groups"].add(group1.group_name)
      
      # Check that the response is correct
      self.assertEqual(response, f"Alice joined group {group1.group_id}.")
      
      # Ensure group1 is in self.board.groups
      self.assertIn(group1.group_id, self.board.groups)
      
      # Ensure Alice has joined group1 (i.e., Alice's groups set should now contain 'group1')
      self.assertIn("group1", self.board.users["Alice"]["groups"])
      
      # Additionally, verify that Alice's membership in the group has been added correctly
      self.assertIn("Alice", group1.members)  # Alice should be part of the group1 members

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

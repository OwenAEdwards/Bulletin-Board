import unittest
from bulletin_board import BulletinBoard

class TestBulletinBoard(unittest.TestCase):

    def setUp(self):
        """Set up a new BulletinBoard instance for testing."""
        self.board = BulletinBoard()

    def test_add_user(self):
        """Test adding a new user."""
        response = self.board.add_user("Alice")
        self.assertEqual(response, "Alice added successfully.")
        self.assertIn("Alice", self.board.users)

    def test_add_duplicate_user(self):
        """Test adding a user that already exists."""
        self.board.add_user("Alice")
        response = self.board.add_user("Alice")
        self.assertEqual(response, "Alice is already a member.")

    def test_remove_user(self):
        """Test removing a user."""
        self.board.add_user("Alice")
        response = self.board.remove_user("Alice")
        self.assertEqual(response, "Alice removed successfully.")
        self.assertNotIn("Alice", self.board.users)

    def test_remove_nonexistent_user(self):
        """Test removing a user that does not exist."""
        response = self.board.remove_user("Bob")
        self.assertEqual(response, "Bob is not found.")

    def test_add_post(self):
        """Test adding a post."""
        message_id = self.board.add_post("Alice", "2024-10-01", "Subject", "Hello World")
        self.assertEqual(message_id, 1)
        self.assertEqual(len(self.board.messages), 1)

    def test_get_message_content(self):
        """Test retrieving message content by ID."""
        self.board.add_post("Alice", "2024-10-01", "Subject", "Hello World")
        content = self.board.get_message_content(1)
        self.assertEqual(content, "Alice on 2024-10-01: Subject")

    def test_get_nonexistent_message_content(self):
        """Test retrieving content of a message that does not exist."""
        content = self.board.get_message_content(999)
        self.assertIsNone(content)

    def test_list_users(self):
        """Test listing users."""
        self.board.add_user("Alice")
        self.board.add_user("Bob")
        users = self.board.list_users()
        self.assertEqual(users, ["Alice", "Bob"])

    def test_join_group(self):
        """Test a user joining a group."""
        self.board.add_user("Alice")
        response = self.board.join_group("Alice", "group1")
        self.assertEqual(response, "Alice joined group group1.")
        self.assertIn("group1", self.board.groups)
        self.assertIn("group1", self.board.users["Alice"]["groups"])

    def test_post_to_group(self):
      """Test posting a message to a group."""
      self.board.add_user("Alice")
      self.board.join_group("Alice", "group1")
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
      self.board.add_user("Alice")
      self.board.join_group("Alice", "group1")
      response = self.board.leave_group("Alice", "group1")
      self.assertEqual(response, "Alice left group group1.")
      self.assertNotIn("group1", self.board.users["Alice"]["groups"])
      self.assertNotIn("Alice", self.board.groups.get("group1", []))

    def test_list_group_users(self):
        """Test listing users in a group."""
        self.board.add_user("Alice")
        self.board.add_user("Bob")
        self.board.join_group("Alice", "group1")
        self.board.join_group("Bob", "group1")
        group_users = self.board.list_group_users("group1")
        self.assertEqual(set(group_users), {"Alice", "Bob"})

    def test_get_group_message(self):
      """Test retrieving a message from a group by message ID."""
      self.board.add_user("Alice")
      self.board.join_group("Alice", "group1")
      message_id = self.board.post_to_group("group1", "Group Subject", "Group Content")
      message_content = self.board.get_group_message("group1", message_id)
      self.assertEqual(message_content, "Group Subject: Group Content")

    def test_get_group_message_not_found(self):
        """Test retrieving a message from a group that does not exist."""
        response = self.board.get_group_message("group1", 999)
        self.assertEqual(response, "Message 999 not found in group group1.")

if __name__ == "__main__":
    unittest.main()

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

if __name__ == "__main__":
    unittest.main()

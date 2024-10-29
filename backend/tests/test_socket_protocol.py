import unittest
from socket_protocol import format_bulletin_message, format_client_command, parse_client_command, parse_bulletin_message

class TestSocketProtocol(unittest.TestCase):

    def test_format_bulletin_message(self):
        """Test formatting a bulletin message."""
        message_id = 1
        sender = "Alice"
        post_date = "2024-10-01"
        subject = "Hello World"
        formatted_message = format_bulletin_message(message_id, sender, post_date, subject)
        expected_message = "1 Alice 2024-10-01 Hello World"
        self.assertEqual(formatted_message, expected_message)

    def test_format_client_command(self):
        """Test formatting a client command."""
        command = "%%connect"
        params = ("Hello", "World")
        formatted_command = format_client_command(command, *params)
        expected_command = "%%connect Hello World"
        self.assertEqual(formatted_command, expected_command)

    def test_parse_client_command_with_params(self):
      """Test parsing a client command with parameters."""
      message = "%join Alice"
      command, params = parse_client_command(message)
      self.assertEqual(command, "%join")
      self.assertEqual(params, ["Alice"])  # This should work correctly as %join expects parameters

    def test_parse_client_command_with_no_params(self):
        """Test parsing a client command with no parameters."""
        message = "%%connect"
        command, params = parse_client_command(message)
        self.assertEqual(command, "%%connect")
        self.assertEqual(params, [])

    def test_parse_bulletin_message(self):
        """Test parsing a bulletin message."""
        message = "1 Alice 2024-10-01 Hello World"
        parsed_message = parse_bulletin_message(message)
        expected_output = {
            'message_id': '1',
            'sender': 'Alice',
            'post_date': '2024-10-01',
            'subject': 'Hello World'
        }
        self.assertEqual(parsed_message, expected_output)

    def test_parse_bulletin_message_with_extra_commas(self):
        """Test parsing a bulletin message with commas in the subject."""
        message = "2 Bob 2024-10-02 Hello, World!"
        parsed_message = parse_bulletin_message(message)
        expected_output = {
            'message_id': '2',
            'sender': 'Bob',
            'post_date': '2024-10-02',
            'subject': 'Hello, World!'
        }
        self.assertEqual(parsed_message, expected_output)

    def test_parse_bulletin_message_invalid_format(self):
        """Test parsing a bulletin message with invalid format."""
        message = "Invalid Message"
        parsed_message = parse_bulletin_message(message)
        self.assertIsNone(parsed_message)

    def test_parse_bulletin_message_missing_parts(self):
        """Test parsing a bulletin message with missing parts."""
        message = "1 Alice 2024-10-01"
        parsed_message = parse_bulletin_message(message)
        self.assertIsNone(parsed_message)

if __name__ == "__main__":
    unittest.main()
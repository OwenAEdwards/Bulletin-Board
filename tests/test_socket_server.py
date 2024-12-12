import unittest
from unittest.mock import patch, MagicMock
import socket_server

class TestSocketServer(unittest.TestCase):

    @patch('socket_server.BulletinBoard')
    def test_handle_client_join(self, MockBulletinBoard):
        mock_bulletin_board = MockBulletinBoard.return_value
        mock_client_socket = MagicMock()
        private_boards = MagicMock()  # Mock for private_boards
        mock_client_socket.recv.side_effect = [
            b'%join username',  # Simulate the join command from the client
            b'%exit'           # Simulate the exit command
        ]

        # Set up the mock to respond as expected
        mock_bulletin_board.add_user.return_value = None  # Ensure it doesn't return anything

        # Call the function
        socket_server.handle_client(mock_client_socket, mock_bulletin_board, private_boards)

        # Check that add_user was called with the expected parameter
        mock_bulletin_board.add_user.assert_called_once_with('username')

        # Check that the correct message was sent to the client
        mock_client_socket.send.assert_any_call(b'username has joined the bulletin board.\r\n')
        mock_client_socket.send.assert_called_with(b'Goodbye!\r\n')  # Ensure the exit message is also checked

    @patch('socket_server.BulletinBoard')
    def test_post_message(self, MockBulletinBoard):
        mock_bulletin_board = MockBulletinBoard.return_value
        mock_client_socket = MagicMock()
        private_boards = MagicMock()  # Mock for private_boards
        mock_client_socket.recv.side_effect = [
            b'%join username',  # First command to join
            b'%post Alice 2024-10-28 12:00 Subject | Content',  # Post command after user joins
            b'%exit'  # Exit command to end the client session
        ]

        # Set up the mock to return a message ID when add_post is called
        mock_bulletin_board.add_post.return_value = 1
        mock_bulletin_board.list_users.return_value = ['Alice']  # Simulate that 'Alice' has joined

        # Call the function
        socket_server.handle_client(mock_client_socket, mock_bulletin_board, private_boards)

        # Check that add_post was called with the expected parameters
        mock_bulletin_board.add_post.assert_called_once_with('Alice', '2024-10-28 12:00', 'Subject', 'Content')

        # Assert that the send call with the expected message was made
        mock_client_socket.send.assert_any_call(b'Message posted with ID 1.\r\n')  # Allow for other calls, too
        mock_client_socket.send.assert_called_with(b'Goodbye!\r\n')  # Verify the exit message

    def test_exit_command(self):
        mock_client_socket = MagicMock()
        mock_bulletin_board = MagicMock()
        private_boards = MagicMock()  # Mock for private_boards
        mock_client_socket.recv.return_value = b'%exit'

        socket_server.handle_client(mock_client_socket, mock_bulletin_board, private_boards)

        mock_client_socket.send.assert_called_with(b'Goodbye!\r\n')

    def test_unknown_command(self):
        mock_client_socket = MagicMock()
        mock_bulletin_board = MagicMock()
        private_boards = MagicMock()  # Mock for private_boards
        mock_client_socket.recv.side_effect = [
            b'%unknown',
            b'%exit'
        ]

        socket_server.handle_client(mock_client_socket, mock_bulletin_board, private_boards)

        mock_client_socket.send.assert_any_call(b'Unknown command.\r\n')
        mock_client_socket.send.assert_called_with(b'Goodbye!\r\n')

    @patch('socket_server.PrivateBoard')
    @patch('socket_server.client_sessions')
    def test_private_board_join(self, mock_client_sessions, MockPrivateBoard):
        mock_private_board = MockPrivateBoard.return_value
        mock_client_socket = MagicMock()

        # Initialize the private_boards as a list of PrivateBoard instances
        mock_private_board.group_id = 1  # Ensure that the group ID matches the command's parameter
        private_boards = [mock_private_board]  # Mock for private_boards list
        
        # Set up the mock client commands
        mock_client_socket.recv.side_effect = [
            b'%join username',  # Simulate joining the public board with a username
            b'%groupjoin 1',    # Simulate a private group join command (group_id = 1)
            b'%exit'            # Simulate exit after the commands
        ]
        
        # Set the username for the mock client in client_sessions
        mock_client_sessions.__getitem__.return_value = {'username': 'username'}
        
        # Set up the mock behavior for join_group
        mock_private_board.join_group.return_value = "username joined group 1."
        
        # Call the function being tested
        socket_server.handle_client(mock_client_socket, MagicMock(), private_boards)

        # Ensure join_group is called once with the expected arguments
        mock_private_board.join_group.assert_called_once_with('username', 1)  # Group ID is 1
        
        # Check if the correct response is sent to the client
        mock_client_socket.send.assert_any_call(b'username joined group 1.\r\n')
        
        # Ensure the exit message is also sent
        mock_client_socket.send.assert_called_with(b'Goodbye!\r\n')

if __name__ == '__main__':
    unittest.main()

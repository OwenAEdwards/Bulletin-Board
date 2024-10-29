import unittest
from unittest.mock import patch, MagicMock
import socket_server

class TestSocketServer(unittest.TestCase):

    @patch('socket_server.BulletinBoard')
    def test_handle_client_join(self, MockBulletinBoard):
        mock_bulletin_board = MockBulletinBoard.return_value
        mock_client_socket = MagicMock()
        mock_client_socket.recv.side_effect = [
            b'%join username',  # Simulate the join command from the client
            b'%%exit'           # Simulate the exit command
        ]

        # Set up the mock to respond as expected
        mock_bulletin_board.add_user.return_value = None  # Ensure it doesn't return anything

        # Call the function
        socket_server.handle_client(mock_client_socket, mock_bulletin_board)

        # Check that add_user was called with the expected parameter
        mock_bulletin_board.add_user.assert_called_once_with('username')

        # Check that the correct message was sent to the client
        mock_client_socket.send.assert_any_call(b'username has joined the bulletin board.')
        mock_client_socket.send.assert_called_with(b'Goodbye!')  # Ensure the exit message is also checked

        print("Add user called:", mock_bulletin_board.add_user.called)  # Debug output

    @patch('socket_server.BulletinBoard')
    def test_post_message(self, MockBulletinBoard):
        mock_bulletin_board = MockBulletinBoard.return_value
        mock_client_socket = MagicMock()
        mock_client_socket.recv.side_effect = [
            b'%post Alice 2024-10-28 Test Subject',  # First command to post
            b'%%exit'  # Exit command to end the client session
        ]

        # Set up the mock to return a message ID when add_post is called
        mock_bulletin_board.add_post.return_value = 1

        # Call the function
        socket_server.handle_client(mock_client_socket, mock_bulletin_board)

        # Check that add_post was called with the expected parameters
        mock_bulletin_board.add_post.assert_called_once_with('Alice', '2024-10-28', 'Test Subject')
        
        # Assert that the send call with the expected message was made
        mock_client_socket.send.assert_any_call(b'Message posted with ID 1.')  # Allow for other calls, too
        mock_client_socket.send.assert_called_with(b'Goodbye!')  # Verify the exit message
        print("Add post called:", mock_bulletin_board.add_post.called)  # Debug output

    def test_exit_command(self):
        mock_client_socket = MagicMock()
        mock_bulletin_board = MagicMock()
        mock_client_socket.recv.return_value = b'%%exit'

        socket_server.handle_client(mock_client_socket, mock_bulletin_board)

        mock_client_socket.send.assert_called_with(b'Goodbye!')

    def test_unknown_command(self):
        mock_client_socket = MagicMock()
        mock_bulletin_board = MagicMock()
        mock_client_socket.recv.side_effect = [
            b'%%unknown',
            b'%%exit'
        ]

        socket_server.handle_client(mock_client_socket, mock_bulletin_board)

        mock_client_socket.send.assert_any_call(b'Unknown command.')
        mock_client_socket.send.assert_called_with(b'Goodbye!')

if __name__ == '__main__':
    unittest.main()
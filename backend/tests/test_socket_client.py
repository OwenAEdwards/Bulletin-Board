import unittest
from unittest.mock import patch, MagicMock
import socket_client

class TestSocketClient(unittest.TestCase):

    @patch('socket_client.socket.socket')
    def test_connect_to_server(self, mock_socket):
        mock_socket.return_value.connect.return_value = None  # Simulate a successful connection
        client_socket = socket_client.connect_to_server('localhost', 12345)
        self.assertIsNotNone(client_socket)
        mock_socket.return_value.connect.assert_called_once_with(('localhost', 12345))

    @patch('socket_client.send_command')
    def test_send_command(self, mock_send_command):
        client_socket = MagicMock()  # Create a mock socket
        command = '%%connect'
        params = ['localhost', '12345']
        
        socket_client.send_command(client_socket, command, *params)
        mock_send_command.assert_called_once_with(client_socket, command, *params)

    @patch('socket_client.socket.socket')
    def test_receive_response(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket

        mock_client_socket.recv.return_value = b'OK'  # Set up recv to return 'OK'
        response = socket_client.receive_response(mock_client_socket)

        mock_client_socket.recv.assert_called_once()  # Assert that recv was called once
        self.assertEqual(response, 'OK')  # Check the returned response
        # Here, you might want to assert that parse_bulletin_message was called if your function does that
        # mock_parse.assert_called_once_with('OK') # Uncomment if needed after adding the patch

    def test_parse_command(self):
        client_socket = MagicMock()  # Create a mock socket

        # Test %%connect command
        self.assertTrue(socket_client.parse_command('%%connect localhost 12345', client_socket))

        # Test %join command
        self.assertTrue(socket_client.parse_command('%join username', client_socket))

        # Test %post command with valid parameters
        self.assertTrue(socket_client.parse_command('%post Alice 2024-10-28 Subject', client_socket))

        # Test %%users command
        self.assertTrue(socket_client.parse_command('%%users', client_socket))

        # Test %%leave command
        self.assertTrue(socket_client.parse_command('%%leave username', client_socket))

        # Test %message command
        self.assertTrue(socket_client.parse_command('%message 1', client_socket))

        # Test %%exit command
        self.assertFalse(socket_client.parse_command('%%exit', client_socket))

        # Test invalid command
        self.assertTrue(socket_client.parse_command('%%invalid', client_socket))


if __name__ == '__main__':
    unittest.main()
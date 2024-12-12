import unittest
from unittest.mock import patch, MagicMock
import socket_client

class TestSocketClient(unittest.TestCase):

    @patch('socket_client.socket.socket')
    async def test_connect_to_server(self, mock_socket):
        mock_socket.return_value.connect.return_value = None  # Simulate a successful connection
        client_socket = socket_client.connect_to_server('localhost', 12345)
        self.assertIsNotNone(client_socket)
        mock_socket.return_value.connect.assert_called_once_with(('localhost', 12345))

    @patch('socket_client.send_command')
    async def test_send_command(self, mock_send_command):
        client_socket = MagicMock()  # Create a mock socket
        command = '%connect'
        params = ['localhost', '12345']
        
        socket_client.send_command(client_socket, command, *params)
        mock_send_command.assert_called_once_with(client_socket, command, *params)

    @patch('socket_client.socket.socket')
    async def test_receive_response(self, mock_socket):
        mock_client_socket = MagicMock()
        mock_socket.return_value = mock_client_socket

        mock_client_socket.recv.return_value = b'OK\r\n'  # Set up recv to return 'OK'
        response = await socket_client.receive_response(mock_client_socket)

        mock_client_socket.recv.assert_called_once()  # Assert that recv was called once
        self.assertEqual(response, 'OK\r\n')  # Check the returned response
        # Here, you might want to assert that parse_bulletin_message was called if your function does that
        # mock_parse.assert_called_once_with('OK') # Uncomment if needed after adding the patch

    @patch('socket_client.connect_to_server')
    async def test_parse_command(self, mock_connect_to_server):
                # Mock the behavior of connect_to_server to return a mock socket
        mock_socket = MagicMock()
        mock_connect_to_server.return_value = mock_socket

        # Start with no connection
        client_socket = None

        # Test %connect command
        client_socket = await socket_client.parse_command('%connect localhost 12345', client_socket)
        self.assertIsNotNone(client_socket)  # Check that client_socket is not None after connecting

        # Test %join command
        client_socket = await socket_client.parse_command('%join username', client_socket)
        self.assertIsNotNone(client_socket)

        # Test %post command with valid parameters
        client_socket = await socket_client.parse_command('%post Alice 2024-10-28 Subject', client_socket)
        self.assertIsNotNone(client_socket)

        # Test %users command
        client_socket = await socket_client.parse_command('%users', client_socket)
        self.assertIsNotNone(client_socket)

        # Test %leave command
        client_socket = await socket_client.parse_command('%leave username', client_socket)
        self.assertIsNotNone(client_socket)

        # Test %message command
        client_socket = await socket_client.parse_command('%message 1', client_socket)
        self.assertIsNotNone(client_socket)

        # Test %exit command
        client_socket = await socket_client.parse_command('%exit', client_socket)
        self.assertFalse(client_socket)  # Expect client_socket to be None after exit

        # Test invalid command
        client_socket = await socket_client.parse_command('%invalid', client_socket)
        self.assertIsNotNone(client_socket)  # Invalid command shouldn't close the socket


if __name__ == '__main__':
    unittest.main()

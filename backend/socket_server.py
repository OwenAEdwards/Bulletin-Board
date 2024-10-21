import socket
import threading
from socket_protocol import format_message, parse_message
from bulletin_board import BulletinBoard

def handle_client(client_socket, bulletin_board):
    # Handle client communication
    pass

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")
    bulletin_board = BulletinBoard()

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, bulletin_board))
        client_handler.start()

def parse_command(command):
    if command.startswith('%%connect'):
        pass
      # Handle connect
    elif command.startswith('%join'):
      # Handle join
      pass
    # Add other commands here
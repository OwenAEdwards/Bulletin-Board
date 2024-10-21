import socket
from socket_protocol import parse_message

def parse_command(command):
    if command.startswith('%connect'):
        # Handle connect command
        pass
    elif command.startswith('%join'):
        # Handle join command
        pass
    # Handle other commands...

def main():
    while True:
        command = input("Enter command: ")
        parse_command(command)

if __name__ == "__main__":
    main()

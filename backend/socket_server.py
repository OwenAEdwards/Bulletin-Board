import socket
import threading
from socket_protocol import parse_client_command
from bulletin_board import BulletinBoard
from private_board import PrivateBoard

# Unique delimiter
CRLF = "\r\n"

# Dictionary to keep track of session data for each client
client_sessions = {}

def handle_client(client_socket, public_board, private_boards):
    """
    Handles communication with a single connected client.
    Continuously listens for client commands, processes them, and sends responses back.
    """
    # Initialize client session data
    client_sessions[client_socket] = {'username': None}
    try:
        # Continuously listen for client commands in a loop.
        while True:
            # Receive up to 1024 bytes from the client.
            message = client_socket.recv(1024).decode('utf-8')

            # If we receive an empty message, continue waiting for a valid message.
            if not message.strip():
                continue

            # Parse the command and parameters from the client's message.
            print(f"Raw message received: {message}")  # Debugging info.
            command, params = parse_client_command(message)
            print(f"Command: {command}, Params: {params}")  # Debugging line

            # Handle the different commands the client can send.
            if command == '%connect':
                # Connect command expected two parameters: address and port.
                if len(params) == 3:
                    address = params[0]
                    port = params[1]
                    username = params[2]

                    # Set username in session data
                    client_sessions[client_socket]['username'] = username

                    response = f"Connected to the bulletin board server at {address}:{port}."
                else:
                    response = "Error: %connect requires address and port."
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%join':
                print("Calling add_user with:", username)
                # Add the user to the bulletin board.
                public_board.add_user(username)
                response = f"{username} has joined the bulletin board. Users active on this board: {public_board.list_users()}"
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%post':
                # Ensure the client has provided the correct number of parameters (sender, post_date, subject, content)
                if len(params) == 4:
                    sender = params[0]
                    post_date = params[1]
                    subject = params[2]
                    content = params[3]

                    # Verify that the sender has joined the bulletin board
                    if sender not in public_board.list_users():
                        response = "Error: You must join the bulletin board first using %join <username>."
                    else:
                        # Generate a unique message ID and add the post to the bulletin board
                        message_id = public_board.add_post(sender, post_date, subject, content)
                        print(f"Calling add_post with: sender={sender}, post_date={post_date}, subject={subject}")
                        
                        response = f"Message posted with ID {message_id}."
                        print(f"[DEBUG] %post response: {response}")
                else:
                    # Error message if the wrong number of parameters is provided
                    response = "Error: Incorrect parameters for %post. Usage: %post <subject>|<content>."
                client_socket.send((response + CRLF).encode('utf-8'))


            elif command == '%users':
                # Retrieve the list of users from the bulletin board.
                users = public_board.list_users()
                # Format the list of users as a newline-separated string if there are any users.
                # If the list is empty, send a response indicating no users are in the group.
                response = "\n".join(users) if users else "No users in the group."
                client_socket.send((response + CRLF).encode('utf-8'))

            # Handle the %leave command to remove the user
            elif command == '%leave':
                username = client_sessions[client_socket].get('username')
                if username:
                    public_board.remove_user(username)
                    response = f"{username} has left the bulletin board."
                    # Clear session data
                    client_sessions[client_socket]['username'] = None
                else:
                    response = "Error: You are not currently joined to leave."
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%message':
                # Message command expects one parameter: message_id.
                if len(params) == 1:
                    message_id = int(params[0])
                    # Retrieve the content of the specified message from the bulletin board.
                    message_content = public_board.get_message_content(message_id)
                    # If the message is found, send its content; otherwise, indicate that it wasn't found.
                    response = message_content if message_content else "Message not found."
                else:
                    # Error message if the wrong number of parameters is provided.
                    response = "Error: %message requires a message ID."
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%exit':
                # Exit command terminates client session.
                # Send a farewell message to the client.
                response = "Goodbye!"
                client_socket.send((response + CRLF).encode('utf-8'))
                # Break the loop to end the connection with the client.
                break

            ### Part 2 commands ###
            
            elif command == '%groups':
                # Ensure private_boards is a list of PrivateBoard instances
                if private_boards:
                    # Retrieve group names and IDs from each PrivateBoard instance
                    groups = [f"ID: {board.group_id}, Name: {board.group_name}" for board in private_boards]
                    # Format the list as a newline-separated string if there are groups available
                    response = "\n".join(groups)
                else:
                    # Indicate that no groups are available
                    response = "No groups available."
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%groupjoin':
                # Group Join command expects one parameter: group_id or group_name.
                if len(params) == 1:
                    group_id = int(params[0])

                    # Check if client already has a username from %join
                    if client_sessions[client_socket]['username']:
                        username = client_sessions[client_socket]['username']

                    # Check if the group exists in private_boards
                    matching_group = next((board for board in private_boards if board.group_id == group_id), None)
                    if matching_group:
                        # Attempt to join the specified group by ID
                        response = matching_group.join_group(username, group_id)
                    else:
                        # Error message if the group does not exist
                        response = f"Error: Group '{group_id}' does not exist."
                else:
                    # Error message if the wrong number of parameters is provided.
                    response = "Error: %groupjoin requires group ID."
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%grouppost':
                # Unpack parsed parameters: sender, post_date, group_id, subject, content.
                if len(params) != 5:
                    response = "Error: Invalid parameters for %grouppost."
                else:
                    sender, post_date, group_id, subject, content = params
                    group_id = int(group_id)

                    # Validate the sender is in the session and joined the server.
                    if not client_sessions[client_socket].get('username') or client_sessions[client_socket]['username'] != sender:
                        response = "Error: You must join the bulletin board first using %join <username>."
                    else:
                        # Check if the group exists in `private_boards`.
                        target_board = next((board for board in private_boards if board.group_id == group_id), None)

                        if target_board is None:
                            response = f"Error: Group '{group_id}' does not exist."
                        elif sender not in target_board.members:
                            # Ensure the sender is a member of the group.
                            response = f"Error: You are not a member of the group '{group_id}'."
                        else:
                            # Add the post to the specified group's private board.
                            message_id = target_board.post_to_group(sender, post_date, subject, content)
                            response = f"Group message posted with ID {message_id} to group '{group_id}'."

                # Send the response back to the client.
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%groupusers':
                # Ensure the command has exactly one parameter (the group ID/name).
                if len(params) == 1:
                    group_id = int(params[0].strip())

                    # Find the target group by group ID.
                    target_board = next((board for board in private_boards if board.group_id == group_id), None)
                    
                    if not target_board:
                        # If the group does not exist, send an error message.
                        response = f"Error: Group '{group_id}' does not exist."
                    else:
                        # Retrieve the list of users in the group.
                        users = target_board.members
                        # Format the list of users as a newline-separated string, or send an appropriate response if empty.
                        response = "\n".join(users) if users else f"No users in group '{group_id}'."
                else:
                    # Error response for incorrect usage.
                    response = "Error: %groupusers requires exactly one parameter: group ID."

                # Send the response back to the client.
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%groupleave':
                # Ensure the command has exactly one parameter (the group ID/name).
                if len(params) == 1:
                    group_id = int(params[0].strip())

                    # Find the target group by group ID.
                    target_board = next((board for board in private_boards if board.group_id == group_id), None)

                    if not target_board:
                        # If the group does not exist, send an error message.
                        response = f"Error: Group '{group_id}' does not exist."
                    else:
                        # Check if the user is part of the group.
                        if username in target_board.members:
                            # Remove the user from the group.
                            target_board.members.remove(username)
                            response = f"{username} has left group {group_id}."
                            
                            # If the group is now empty, delete it.
                            if not target_board.members:
                                private_boards.remove(target_board)
                                response += f" Group {group_id} has been deleted as it has no members."
                        else:
                            # User is not a member of the group.
                            response = f"Error: {username} is not a member of group '{group_id}'."
                else:
                    # Error response for incorrect usage.
                    response = "Error: %groupleave requires exactly one parameter: group ID."

                # Send the response back to the client.
                client_socket.send((response + CRLF).encode('utf-8'))

            elif command == '%groupmessage':
                # Ensure the command has the correct number of parameters.
                if len(params) == 2:
                    group_id, message_id = params
                    group_id = group_id.strip()
                    message_id = message_id.strip()

                    # Validate numeric parameters.
                    if not group_id.isdigit() or not message_id.isdigit():
                        response = "Error: Group ID and Message ID must be numeric."
                    else:
                        group_id = int(group_id)
                        # Find the target group by group ID.
                        target_board = next((board for board in private_boards if board.group_id == group_id), None)
                        
                        if not target_board:
                            response = f"Error: Group '{group_id}' does not exist."
                        else:
                            # Retrieve the message from the group.
                            message = target_board.get_group_message(int(group_id), int(message_id))
                            response = message  # The `get_group_message` method returns the appropriate message or an error.
                else:
                    response = "Error: %groupmessage requires exactly 2 parameters: group ID and message ID."

                # Send the response back to the client.
                client_socket.send((response + CRLF).encode('utf-8'))

            else:
                # Send an error response if the command is not recognized.
                response = "Unknown command."
                client_socket.send((response + CRLF).encode('utf-8'))
    
    except ValueError as ve:
        print(f"ValueError encountered: {ve}")
        response = "Error: Invalid parameters."
        client_socket.send((response + CRLF).encode('utf-8'))
    except socket.error as se:
        print(f"Socket error: {se}")
        response = "Error: Socket communication failure."
        client_socket.send((response + CRLF).encode('utf-8'))
    except Exception as e:
        print(f"Unexpected error handling client: {e}")
    finally:
        # Clean up session data
        if client_socket in client_sessions:
            del client_sessions[client_socket]
        # Ensure the client socket is closed, whether or not an error occurred.
        # This releases resources associated with the client connection.
        client_socket.close()
        print("Client disconnected.")

def start_server(host, port):
    """
    Initializes and starts the server, listening for client connections.
    Spawns a new thread for each connected client to handle communications.
    """

    # Create a new socket using IPv4 (AF_INET) and TCP (SOCK_STREAM).
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server to the specified host and port.
    server.bind((host, port))

    # Start listening for incoming connections; '5' is the max number of queued connections.
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    # Initialize a BulletinBoard instance to store messages from clients for the public bulletin board.
    public_board = BulletinBoard()

    # Initialize 5 BulletinBoard instances to store messages from clients for the private bulletin boards.
    custom_group_names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
    private_boards = [PrivateBoard(f"Group {name}") for name in custom_group_names]

    # Continuously accept new client connections.
    while True:
        # Accept a new client connection; returns a new socket and the address of the client.
        client_socket, client_address = server.accept()
        print(f"[*] Accepted connection from {client_address}")

        # Create a new thread to handle communication with this client.
        # Each client connection is managed independently to allow simultaneous clients.
        client_handler_thread = threading.Thread(target=handle_client, args=(client_socket, public_board, private_boards))

        # Start the client handler thread.
        client_handler_thread.start()

if __name__ == "__main__":
    start_server('127.0.0.1', 5000)  # or 'localhost'
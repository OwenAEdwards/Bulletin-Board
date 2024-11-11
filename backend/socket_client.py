import socket
from socket_protocol import format_client_command, parse_bulletin_message

def connect_to_server(host, port):
    """
    Establishes a connection to the server and returns the connected socket.
    """
    # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM).
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to establish a connection to the specified host and port.
    client_socket.connect((host, port))

    # If successful, print a confirmation message.
    print("Connected to the server.")

    # Return the connected socket for further communication.
    return client_socket

def send_command(client_socket, command, *params):
    """
    Sends a formatted command to the server.
    """
    # Format the command and parameters into a single string, using format_client_command.
    formatted_command = format_client_command(command, *params)

    # Send only if formatted_command is not empty
    if formatted_command:
        # Encode the formatted command as a UTF-8 byte string and send it through the socket.
        client_socket.send(formatted_command.encode('utf-8'))

        # Print the formatted command to the console for confirmation and debugging.
        print(f"Sent: {formatted_command}")
    else:
        print("Attempted to send an empty command, skipping send.")

def receive_response(client_socket):
    """
    Receives and handles responses from the server.
    If the response is a bulletin message (i.e., from a %post command), it parses and formats it accordingly.
    """
    try:
        # Receive a response from the server (up to 1024 bytes) and decode it to a UTF-8 string.
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Raw Response: {response}")

        if not response:
            print("Received empty response, server might have closed the connection.")
            return

        # Check if the response is a bulletin message based on the expected format.
        if response.startswith('%post '):
            parsed_message = parse_bulletin_message(response)
            if parsed_message:
                # If successfully parsed, print each part of the bulletin message with labeled output.
                print("Parsed Bulletin Message:")
                for key, value in parsed_message.items():
                    print(f"{key}: {value}")
            else:
                print("Failed to parse bulletin message.")
        else:
            # If it's not a bulletin message, print as a regular response.
            print("Response:", response)

        # Return the response for further assertions in tests.
        return response
    except socket.error as e:
        print(f"Error receiving response: {e}")


def parse_command(command, client_socket):
    """
    Parses and sends commands based on user input.
    """
    # Handle the %connect command, splitting additional parameters if provided.
    if command.startswith('%connect'):
        params = command.split()[1:]  # Capture any additional parameters.
        if len(params) != 2:
            print("Usage: %connect <address> <port>")
            return client_socket
        host, port = params
        try:
            port = int(port)  # Convert port to integer
            # Attempt to connect to the server
            client_socket = connect_to_server(host, port)
            # print("client_socket, inside parse_command(), is:",client_socket)
        except Exception as e:
            print(f"Failed to connect: {e}")
            client_socket = None
            return client_socket
        # Send the %connect command to the server with any extra parameters.
        send_command(client_socket, '%connect', *params)
        return client_socket
        # print("client_socket, after sending data, is:",client_socket)

    # Handle the %join command to join with a specified username.
    elif command.startswith('%join'):
        username = command.split()[1]
        # Send the %join command along with the specified username to the server.
        send_command(client_socket, '%join', username)

    # Handle the %post command, verifying the correct number of arguments.
    elif command.startswith('%post'):
        parts = command.split(maxsplit=3)  # Split command to capture all arguments.
        # Validate if all necessary parts (sender, date, subject) are provided.
        if len(parts) < 4:
            print("Usage: %post <sender> <post_date> <subject>")
            return client_socket
        # Unpack the command arguments.
        _, sender, post_date, subject = parts
        # Send the %post command with sender, date, and subject to create a new post.
        send_command(client_socket, '%post', sender, post_date, subject)

    # Handle the %users command to request the list of users.
    elif command.startswith('%users'):
        # Send the %users command to the server without additional parameters
        send_command(client_socket, '%users')

    # Handle the %leave command to leave with a specified username.
    elif command.startswith('%leave'):
        username = command.split()[1]
        # Send the %leave command to disconnect the specified user from the server.
        send_command(client_socket, '%leave', username)

    # Handle the %message command to request a specific message by ID.
    elif command.startswith('%message'):
        message_id = command.split()[1]
        # Send the %message command to retrieve the message with the specified ID.
        send_command(client_socket, '%message', message_id)

    # Handle the %exit command to close the connection and end the program.
    elif command.startswith('%exit'):
        # Send the %exit command to the server to close the connection.
        send_command(client_socket, '%exit')
        print("Exiting.")
        # Close the socket connection.
        client_socket.close()
        client_socket = False
        # Return False to stop further command parsing.
        return client_socket

    ### Part 2 Commands ###
    
    # Handle the %groups command to list available groups.
    elif command.startswith('%groups'):
        # Send the %groups command to retrieve the list of groups from the server.
        send_command(client_socket, '%groups')

    # Handle the %groupjoin command to join a specified group by ID.
    elif command.startswith('%groupjoin'):
        group_id = command.split()[1]
        # Send the %groupjoin command with the specified group ID to join the group.
        send_command(client_socket, '%groupjoin', group_id)

    # Handle the %grouppost command, checking for all required parameters.
    elif command.startswith('%grouppost'):
        parts = command.split(maxsplit=3)  # Split command to capture all arguments.
        # Validate if all necessary parts (group ID, subject, content) are provided.
        if len(parts) < 4:
            print("Usage: %grouppost <group_id> <subject> <content>")
            # Exit function without sending command if parameters are missing.
            return client_socket
        # Unpack the command arguments.
        _, group_id, subject, content = parts
        # Send the %grouppost command with group ID, subject, and content to post in the group.
        send_command(client_socket, '%grouppost', group_id, subject, content)

    # Handle the %groupusers command to list users in a specified group.
    elif command.startswith('%groupusers'):
        group_id = command.split()[1]
        # Send the %groupusers command with group ID to retrieve the list of users in that group.
        send_command(client_socket, '%groupusers', group_id)

    # Handle the %groupleave command to leave a specified group.
    elif command.startswith('%groupleave'):
        group_id = command.split()[1]
        # Send the %groupleave command with the group ID to disconnect from that group.
        send_command(client_socket, '%groupleave', group_id)

    # Handle the %groupmessage command to get a specific message in a group.
    elif command.startswith('%groupmessage'):
        group_id, message_id = command.split()[1:3]
        # Send the %groupmessage command with both group ID and message ID to fetch the message.
        send_command(client_socket, '%groupmessage', group_id, message_id)

    # Handle unknown commands.
    else:
        print("Unknown command.")
        return client_socket

    # After sending the command, wait for the server's response.
    receive_response(client_socket)
    return client_socket

def main():
    # Startwith no connection.
    client_socket = None

    # Command loop.
    while True:
        command = input("Enter command: ")
        # print("client_socket, inside main(), is:",client_socket)
        # Call parse_command to handle the command and update client_socket.
        if command.startswith('%connect') or client_socket:
            client_socket = parse_command(command, client_socket)
        else:
            # Notify user to connect first if client_socket is None and not using %connect
            print("Please connect to the server first using %connect <address> <port>.")
            continue
        # Break the loop if parse_command returns False (i.e., on %exit command).
        if client_socket is False:
            break

if __name__ == "__main__":
    main()
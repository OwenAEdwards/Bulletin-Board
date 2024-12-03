import socket
import threading
import asyncio
from socket_protocol import format_client_command, parse_bulletin_message

username = None  # Global variable to track the joined username

def connect_to_server(host, port):
    """
    Establishes a connection to the server and returns the connected socket.
    """
    # Create a socket object using IPv4 (AF_INET) and TCP (SOCK_STREAM).
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to establish a connection to the specified host and port.
    client_socket.connect((host, port))

    # Second connection: dedicated signal listening
    signal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    signal_socket.connect((host, port+1))

    # If successful, print a confirmation message.
    print("Connected to the server.")

    # Start a daemon thread to listen for signals
    listener_thread = threading.Thread(target=listen_for_signals, args=(signal_socket,), daemon=True)
    listener_thread.start()

    # Return the connected socket for further communication.
    return client_socket

def listen_for_signals(client_socket):
    """
    Listens for JOIN_SIGNAL or LEAVE_SIGNAL messages from the server.
    """
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8').strip()
            if message:
                print(f"Received: {message}")
                # Check for JOIN_SIGNAL or LEAVE_SIGNAL
                if message.startswith("JOIN_SIGNAL"):
                    _, username = message.split(maxsplit=1)
                    print(f"User joined: {username}")
                elif message.startswith("LEAVE_SIGNAL"):
                    _, username = message.split(maxsplit=1)
                    print(f"User left: {username}")
    except (socket.error, Exception) as e:
        print(f"Signal listening error: {e}")

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
        print(f"Sent: {formatted_command.strip()}")
    else:
        print("Attempted to send an empty command, skipping send.")

async def receive_response(client_socket):
    """
    Receives and processes all responses from the server until no more data is available.
    If the response is a bulletin message, it parses and formats it accordingly.
    """
    loop = asyncio.get_event_loop()
    buffer = ""  # Accumulates data

    try:
        while True:
            # Attempt to receive up to 1024 bytes from the server
            response_part = await loop.sock_recv(client_socket, 1024)

            if not response_part:
                break  # Connection closed by the server
            
            # Decode
            buffer += response_part.decode('utf-8')

            # Process complete message
            while "\r\n" in buffer:
                message, buffer = buffer.split("\r\n", 1)
            return message
    except Exception as e:
        print("Error during receive:", e)

    # Combine all parts to form the complete response
    response = ''.join(message)
    print(f"Raw Full Response:", response)

    # Handle and display the response as appropriate
    if response.startswith('%post '):
        parsed_message = parse_bulletin_message(response)
        if parsed_message:
            print("Parsed Bulletin Message:")
            for key, value in parsed_message.items():
                print(f"{key}: {value}")
        else:
            print("Failed to parse bulletin message.")
    else:
        print("Response:", response)

    return response

async def parse_command(command, client_socket):
    """
    Parses and sends commands based on user input.
    """
    global username

    # Handle the %connect command, splitting additional parameters if provided.
    if command.startswith('%connect'):
        params = command.split()[1:]  # Capture any additional parameters.
        if len(params) < 2:
            print("Usage: %connect <address> <port>")
            return client_socket
        host, port = params
        try:
            port = int(port)  # Convert port to integer
            # Attempt to connect to the server
            client_socket = connect_to_server(host, port)
        except Exception as e:
            print(f"Failed to connect: {e}")
            client_socket = None
            return client_socket
        # Combine host, port, and username into a single string, separated by spaces
        connect_params = f"{host} {port} {username}"
        # Send the %connect command to the server with any extra parameters.
        #print("connect_params", connect_params)
        send_command(client_socket, '%connect', connect_params)
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %connect command:", response)
        return client_socket

    # Handle the %join command to join with a specified username.
    elif command.startswith('%join'):
        # Send the %join command along with the specified username to the server.
        send_command(client_socket, '%join')
        # Wait for server confirmation of join
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %join command:", response)
        return client_socket

    # Handle the %post command, verifying the correct number of arguments.
    elif command.startswith('%post'):
        # Split once using | to separate subject and content
        try:
            _, rest = command.split(maxsplit=1)  # Extract everything after %post
            subject, content = rest.split('|', maxsplit=1)  # Split subject and content by |
            subject = subject.strip()  # Clean up extra whitespace
            content = content.strip()
        except ValueError:
            print("Usage: %post <subject>|<content>")
            return client_socket

        # Generate post date on the client-side for consistency
        from datetime import datetime
        post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Construct the final message with the | separator intact
        final_message = f"%post {username} {post_date} {subject}|{content}"

        # Send the %post command with all parameters to the server.
        send_command(client_socket, final_message)

        # Receive the response after each command
        response = await receive_response(client_socket)

        print("[DEBUG] Response after %post command:", response)
        return client_socket

    # Handle the %users command to request the list of users.
    elif command.startswith('%users'):
        # Send the %users command to the server without additional parameters
        send_command(client_socket, '%users')
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %users command:", response)
        return client_socket

    # Handle the %leave command to leave with a specified username.
    elif command.startswith('%leave'):
        # Send the %leave command to disconnect the specified user from the server.
        send_command(client_socket, '%leave', username)
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %leave command:", response)
        return client_socket

    # Handle the %message command to request a specific message by ID.
    elif command.startswith('%message'):
        # Split the command into parts
        parts = command.split()

        # Check if Message ID is provided
        if len(parts) != 2:
            print("Usage: %message <message_id>")
            return client_socket
        
        message_id = parts[1]
        # Send the %message command to retrieve the message with the specified ID.
        send_command(client_socket, '%message', message_id)
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %message command:", response)
        return client_socket

    # Handle the %exit command to close the connection and end the program.
    elif command.startswith('%exit'):
        # Send the %exit command to the server to close the connection.
        send_command(client_socket, '%exit')
        print("Exiting.")
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %exit command:", response)
        # Close the socket connection.
        client_socket.close()
        client_socket = False
        username = None
        # Return False to stop further command parsing.
        return client_socket

    ### Part 2 Commands ###
    
    # Handle the %groups command to list available groups.
    elif command.startswith('%groups'):
        # Send the %groups command to retrieve the list of groups from the server.
        send_command(client_socket, '%groups')
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %groups command:", response)
        return client_socket

    # Handle the %groupjoin command to join a specified group by ID.
    elif command.startswith('%groupjoin'):
        # Split the command into parts
        parts = command.split()

        # Check if Group ID is provided.
        if len(parts) != 2:
            print("Usage: %groupjoin <group_id>")
            return client_socket

        group_id = parts[1]
        # Send the %groupjoin command with the specified group ID to join the group.
        send_command(client_socket, '%groupjoin', group_id)
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %groupjoin command:", response)
        return client_socket

    # Handle the %grouppost command, verifying the correct number of arguments.
    elif command.startswith('%grouppost'):
        # Split once to separate group ID, subject, and content.
        try:
            _, rest = command.split(maxsplit=1)  # Extract everything after %grouppost
            group_id, rest = rest.split(maxsplit=1)  # Separate group_id from the rest
            subject, content = rest.split('|', maxsplit=1)  # Split subject and content by |
            group_id = group_id.strip()
            subject = subject.strip()
            content = content.strip()
        except ValueError:
            print("Usage: %grouppost <group_id> <subject>|<content>")
            return client_socket

        # Generate post date on the client-side for consistency.
        from datetime import datetime
        post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Construct the final message with the | separator intact.
        final_message = f"%grouppost {username} {post_date} {group_id} {subject}|{content}"

        print("[DEBUG] Client socket before sending %grouppost:", client_socket)

        # Send the %grouppost command with all parameters to the server.
        send_command(client_socket, final_message)

        # Receive the response after each command.
        response = await receive_response(client_socket)

        print("[DEBUG] Response after %grouppost command:", response)
        return client_socket

    # Handle the %groupusers command to list users in a specified group.
    elif command.startswith('%groupusers'):
        try:
            # Parse the command to get the group ID.
            _, group_id = command.split(maxsplit=1)
            group_id = group_id.strip()

            # Send the %groupusers command with the group ID to the server.
            send_command(client_socket, f"%groupusers {group_id}")

            # Receive and display the response from the server.
            response = await receive_response(client_socket)
            print(f"Users in group {group_id}:\n{response}")
            return client_socket
        except ValueError:
            # Error message for invalid command format.
            print("Usage: %groupusers <group_id>")
            return client_socket

    # Handle the %groupleave command to leave a specified group.
    elif command.startswith('%groupleave'):
        try:
            # Parse the command to get the group ID.
            _, group_id = command.split(maxsplit=1)
            group_id = group_id.strip()

            # Send the %groupleave command with the group ID to the server.
            send_command(client_socket, f"%groupleave {group_id}")

            # Receive and display the response from the server.
            response = await receive_response(client_socket)
            print(response)
            return client_socket
        except ValueError:
            # Error message for invalid command format.
            print("Usage: %groupleave <group_id>")
            return client_socket

    # Handle the %groupmessage command to fetch a specific message from a group.
    elif command.startswith('%groupmessage'):
        try:
            # Parse group ID and message ID from the command.
            _, group_id, message_id = command.split(maxsplit=2)
            
            # Validate the parameters.
            group_id = group_id.strip()
            message_id = message_id.strip()
            
            if not group_id.isdigit() or not message_id.isdigit():
                print("Error: Group ID and Message ID must be numeric.")
                return client_socket

            # Construct the command to send to the server.
            final_message = f"%groupmessage {group_id} {message_id}"
            send_command(client_socket, final_message)

            # Await and print the response from the server.
            response = await receive_response(client_socket)
            print(f"[Server Response] {response}")
            return client_socket

        except ValueError:
            print("Usage: %groupmessage <group_id> <message_id>")
            return client_socket

    # Handle unknown commands.
    else:
        print("Unknown command.")
        return client_socket

async def main():
    # Startwith no connection.
    client_socket = None

    # Set username.
    global username
    username = input("Enter username: ")

    # Command loop.
    while True:
        command = input("Enter command: ")
        # Call parse_command to handle the command and update client_socket.
        if command.startswith('%connect') or client_socket:
            client_socket = await parse_command(command, client_socket)
        else:
            # Notify user to connect first if client_socket is None and not using %connect
            print("Please connect to the server first using %connect <address> <port>.")
            continue
        # Break the loop if parse_command returns False (i.e., on %exit command).
        if client_socket is False:
            break

if __name__ == "__main__":
    asyncio.run(main())
import socket
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
        await receive_response(client_socket)
        return client_socket
        # print("client_socket, after sending data, is:",client_socket)

    # Handle the %join command to join with a specified username.
    elif command.startswith('%join'):
        # Prevent joining if already logged in
        if username:
            print("You are already joined as:", username)
            return client_socket
        
        username = command.split()[1]
        print("[DEBUG] Client socket before sending %join:", client_socket)
        # Send the %join command along with the specified username to the server.
        send_command(client_socket, '%join', username)
        # Wait for server confirmation of join
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %join command:", response)
        return client_socket

    # Handle the %post command, verifying the correct number of arguments.
    elif command.startswith('%post'):
        # Validate if the client has joined (username must be defined).
        if not username:
            print("You must join the bulletin board first using %join <username>.")
            return client_socket

        # Split only once after the command to get the subject and content as a single string
        parts = command.split(maxsplit=2)

        # Validate if subject and content are provided.
        if len(parts) < 3:
            print("Usage: %post <subject> <content>")
            return client_socket

        # Extract the subject and content from the split parts
        _, subject, content = parts

        # Generate post date on the client-side for consistency
        from datetime import datetime
        post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Construct the final message with all parts as a single string
        final_message = f"%post {username} {post_date} {subject} {content}"

        print("[DEBUG] Client socket before sending %post:", client_socket)

        # Send the %post command with all parameters to the server.
        send_command(client_socket, final_message)

        # Receive the response after each command
        response = await receive_response(client_socket)

        print("[DEBUG] Response after %post command:", response)
        return client_socket

    # Handle the %users command to request the list of users.
    elif command.startswith('%users'):
        # Validate if the client has joined (username must be defined).
        if not username:
            print("You must join the bulletin board first using %join <username>.")
            return client_socket

        # Send the %users command to the server without additional parameters
        send_command(client_socket, '%users')
        response = await receive_response(client_socket)
        print("[DEBUG] Response after %users command:", response)
        return client_socket

    # Handle the %leave command to leave with a specified username.
    elif command.startswith('%leave'):
        # Check if the client is logged in as a user
        if username:
            # Send the %leave command to disconnect the specified user from the server.
            send_command(client_socket, '%leave', username)
            response = await receive_response(client_socket)
            print("[DEBUG] Response after %leave command:", response)

            # Clear the username afterwards
            username = None
        else:
            print("You are not currently joined.")
        return client_socket

    # Handle the %message command to request a specific message by ID.
    elif command.startswith('%message'):
        # Validate if the client has joined (username must be defined).
        if not username:
            print("You must join the bulletin board first using %join <username>.")
            return client_socket

        # Split the command into parts
        parts = command.split()

        # Check if message ID is provided
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
    await receive_response(client_socket)
    return client_socket

async def main():
    # Startwith no connection.
    client_socket = None

    # Command loop.
    while True:
        command = input("Enter command: ")
        # print("client_socket, inside main(), is:",client_socket)
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
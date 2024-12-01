def format_client_command(command, *params):
    """
    Formats a command message that the client will send to the server.
    Use params tuple to handle multiple possible parameters for different commands.
    """
    return f"{command} " + " ".join(params)

def format_bulletin_message(message_id, sender, post_date, subject, content):
    """
    Formats a bulletin message for display on the server's bulletin board.
    """
    return f"{message_id} {sender} {post_date} {subject} {content}"

def parse_client_command(message):
    """
    Parses a command received by the server from the client into its components.
    This function can handle various commands and their parameters.
    """
    # Strip any extra spaces at the beginning and end of the message.
    message = message.strip()

    # Identify the command and the rest of the message.
    command_parts = message.split(maxsplit=1)  # Split into command and parameters (if any)

    # The first part is the command, so we strip any extra spaces.
    command = command_parts[0].strip()

    # If there are no additional parts, return an empty list for parameters.
    if len(command_parts) == 1:
        return command, []

    # Split the remaining message into parameters.
    params = command_parts[1].split()  # Split the parameters by spaces

    # Handling specific commands based on their structure.
    if command in ['%users', '%leave', '%exit', '%groups']:
        # Commands that do not require parameters
        return command, []

    elif command == '%connect':
        if len(params) != 2:
            print("Usage: %connect <address> <port>")
            return command, []
        return command, [params[0].strip(), params[1].strip()]

    elif command in ['%join', '%message', '%groupjoin', '%groupusers', '%groupleave']:
        # Commands expecting exactly one parameter
        return command, [params[0].strip()] if params else []

    elif command == '%post':
        # Ensure we have the expected number of parameters (sender, post_date, subject|content)
        if len(params) < 4:
            print("Usage: %post <sender> <post_date> <subject>|<content>")
            return command, []
        
        sender = params[0].strip()
        post_date = f"{params[1].strip()} {params[2].strip()}"  # Combine date and time

        try:
            # Combine everything after post_date into one string and split by the first |
            subject_and_content = " ".join(params[3:]).strip()
            subject, content = subject_and_content.split('|', maxsplit=1)
            subject = subject.strip()
            content = content.strip()
        except ValueError:
            # Handle missing | separator
            print("Error: Missing | separator in %post command.")
            return command, []

        return command, [sender, post_date, subject, content]

    elif command == '%grouppost':
        # Ensure we have the expected number of parameters (sender, post_date, group_id, subject|content).
        if len(params) < 5:
            print("Usage: %grouppost <sender> <post_date> <group_id> <subject>|<content>")
            return command, []

        sender = params[0].strip()
        post_date = f"{params[1].strip()} {params[2].strip()}"  # Combine date and time
        group_id = params[3].strip()

        try:
            # Combine everything after group_id into one string and split by the first |
            subject_and_content = " ".join(params[4:]).strip()
            subject, content = subject_and_content.split('|', maxsplit=1)
            subject = subject.strip()
            content = content.strip()
        except ValueError:
            # Handle missing | separator
            print("Error: Missing | separator in %grouppost command.")
            return command, []

        return command, [sender, post_date, group_id, subject, content]

    elif command == '%groupmessage':
        # Command expecting two parameters
        if len(params) < 2:
            return command, []
        return command, params[:2]

    else:
        print("Unknown command.")
        return command, []

def parse_bulletin_message(message):
    """
    Parses a bulletin board message sent by the server to the client.
    """
    try:
        # Attempt to split the message into exactly 4 parts: message_id, sender, post_date, and subject.
        # Splitting only 3 times ensures that the subject can contain spaces without causing issues.
        message_id, sender, post_date, subject = message.split(" ", 3)

        # Return the parsed components in a dictionary, with each value stripped of extra spaces.
        return {
            'message_id': message_id.strip(),
            'sender': sender.strip(),
            'post_date': post_date.strip(),
            'subject': subject.strip()
        }
    except ValueError:
        # If there aren't exactly 4 parts (e.g., if the format is invalid), return None to indicate failure.
        print(f"Failed to parse message: {message}")  # Debugging info
        return None

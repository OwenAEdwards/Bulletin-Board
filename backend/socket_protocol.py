def format_client_command(command, *params):
    """
    Formats a command message that the client will send to the server.
    Use params tuple to handle multiple possible parameters for different commands.
    """
    return f"{command} " + " ".join(params)

def format_bulletin_message(message_id, sender, post_date, subject):
    """
    Formats a bulletin message for display on the server's bulletin board.
    """
    return f"{message_id} {sender} {post_date} {subject}"

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
    if command in ['%%connect', '%%users', '%%exit', '%%groups']:
        # Commands that do not require parameters
        return command, []

    elif command in ['%join', '%%leave', '%%message', '%%groupjoin', '%%groupusers', '%%groupleave']:
        # Commands expecting exactly one parameter
        return command, [params[0].strip()] if params else []

    elif command == '%post':
        # Command expecting three parameters
        if len(params) < 3:
            print("Usage: %post <sender> <post_date> <subject>")
            return command, []
        sender = params[0].strip()
        post_date = params[1].strip()
        subject = " ".join(params[2:]).strip()  # Join all remaining parts as the subject
        return command, [sender, post_date, subject]

    elif command == '%%grouppost':
        # Command expecting three parameters
        if len(params) < 3:
            print("Usage: %%grouppost <group_id> <subject> <content>")
            return command, []
        return command, params[:3]

    elif command == '%%groupmessage':
        # Command expecting two parameters
        if len(params) < 2:
            print("Usage: %%groupmessage <group_id> <message_id>")
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

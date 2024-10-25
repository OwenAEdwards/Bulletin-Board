def format_bulletin_message(message_id, sender, post_date, subject):
    """
    Formats a bulletin message for display on the server's bulletin board.
    """
    return f"{message_id},{sender},{post_date},{subject}"

def format_client_command(command, *params):
    """
    Formats a command message that the client will send to the server.
    Use params tuple to handle multiple possible parameters for different commands
    """
    return f"{command}," + ",".join(params)

def parse_client_command(message):
    """
    Parses a command received by the server from the client into its components.
    Parse commands into a tuple for different commands.
    """

    # Split the incoming message at the first comma (if any). This gives the command 
    # and the rest of the message (parameters).
    parts = message.split(",", 1)

    # The first part is the command (e.g., '%connect'), so we strip any extra spaces.
    command = parts[0].strip()

    # If there are additional parts (i.e., parameters), split them by commas.
    if len(parts) > 1:
        # Split the remaining message into parameters and strip spaces from each.
        params = parts[1].split(",")
        return command, [param.strip() for param in params]
    else:
        # If there are no additional parts, return an empty list for parameters.
        return command, []

def parse_bulletin_message(message):
    """
    Parses a bulletin board message sent by the server to the client.
    """
    try:
        # Attempt to split the message into exactly 4 parts: message_id, sender, post_date, and subject.
        # Splitting only 3 times ensures that the subject can contain commas without causing issues.
        message_id, sender, post_date, subject = message.split(",", 3)

        # Return the parsed components in a dictionary, with each value stripped of extra spaces.
        return {
            'message_id': message_id.strip(),
            'sender': sender.strip(),
            'post_date': post_date.strip(),
            'subject': subject.strip()
        }
    except ValueError:
        # If there aren't exactly 4 parts (e.g., if the format is invalid), return None to indicate failure.
        return None

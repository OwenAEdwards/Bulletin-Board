import itertools

class PrivateBoard:
    group_id_counter = itertools.count(1)  # Class-level counter for unique group IDs

    def __init__(self, group_name):
        self.group_name = group_name  # Unique name for the group
        self.group_id = next(PrivateBoard.group_id_counter)  # Automatically assign a unique group ID
        self.members = set()  # Members with access to this private board
        self.messages = []  # Messages specific to this group
        self.message_counter = itertools.count(1)  # Unique message IDs

    def join_group(self, user, group_id):
        """Adds the user to the specified group, creating the group if it doesn't exist."""
        
        # Ensure the user is not already in the group
        if user not in self.members:
            self.members.add(user)  # Add user to members set
            return f"{user} joined group {group_id}."
        else:
            return f"User {user} is already a member of group {group_id}."

    def post_to_group(self, sender, post_date, subject, content):
        """
        Posts a message to the private group, including sender and post date.
        """
        message_id = next(self.message_counter)
        message = {
            'id': message_id,
            'sender': sender,
            'date': post_date,
            'subject': subject,
            'content': content
        }
        self.messages.append(message)  # Append the message to the group's message list
        return message_id  # Return the unique message ID

    def list_group_users(self, group_id):
        """Returns a list of users in the specified group."""
        if group_id in self.groups:
            return list(self.groups[group_id]['members'])
        return []

    def leave_group(self, user, group_id):
        """
        Removes a user from a specified group.
        """
        if group_id in self.groups and user in self.groups[group_id]['members']:
            self.groups[group_id]['members'].remove(user)
            self.users[user]['groups'].remove(group_id)
            if not self.groups[group_id]['members']:  # Remove group if empty
                del self.groups[group_id]
            return f"{user} left group {group_id}."
        return f"{user} is not in group {group_id}."

    def get_group_message(self, group_id, message_id):
        """
        Retrieves a specific message from a group based on its ID.
        """
        # Search for the message with the given ID.
        for message in self.messages:
            if message['id'] == int(message_id):
                # Format the message summary similar to the public board's `%message`.
                return f"{message['sender']} on {message['date']}: {message['subject']}"
        
        # Return an error if the message is not found.
        return f"Error: Message ID '{message_id}' not found in group '{group_id}'."
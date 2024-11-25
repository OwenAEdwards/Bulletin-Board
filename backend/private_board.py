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
        if user not in self.users:
            return f"User {user} not found."
        
        # Initialize the group with members and messages if it doesn’t exist
        if group_id not in self.groups:
            self.groups[group_id] = {'members': set(), 'messages': []}
        
        # Add user to the group
        self.groups[group_id]['members'].add(user)
        self.users[user]['groups'].add(group_id)
        
        return f"{user} joined group {group_id}."

    def post_to_group(self, group_id, subject, content):
        """
        Posts a message to a specific group, if the group exists.
        """
        if group_id in self.groups:
            message_id = next(self.message_counter)
            message = {
                'id': message_id,
                'subject': subject,
                'content': content
            }
            self.groups[group_id]['messages'].append(message)  # Append message to group's messages list
            return message_id  # Return only the message ID as expected by the test
        return f"Group {group_id} not found."

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
        if group_id in self.groups:
            for message in self.groups[group_id]['messages']:
                if message['id'] == message_id:
                    return f"{message['subject']}: {message['content']}"
        return f"Message {message_id} not found in group {group_id}."
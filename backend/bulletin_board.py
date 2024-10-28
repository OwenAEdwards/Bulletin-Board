import itertools

class BulletinBoard:
    def __init__(self):
        self.users = {}  # Store users in a dictionary for quick access
        self.messages = []  # List to store public messages
        self.groups = {}  # Dictionary to store groups and their members
        self.message_counter = itertools.count(1)  # To assign unique message IDs

    def add_user(self, user):
        """
        Adds a new user to the bulletin board if they are not already present.
        """
        if user not in self.users:
            self.users[user] = {'groups': set()}
            return f"{user} added successfully."
        return f"{user} is already a member."

    def remove_user(self, user):
        """
        Removes a user from the bulletin board and any groups they belong to.
        """
        if user in self.users:
            # Remove user from all groups they belong to
            for group in self.users[user]['groups']:
                self.groups[group].remove(user)
                if not self.groups[group]:  # Remove group if empty
                    del self.groups[group]
            del self.users[user]  # Finally, remove the user from the board
            return f"{user} removed successfully."
        return f"{user} is not found."

    def add_post(self, sender, post_date, subject):
        """
        Creates a new message and assigns it a unique ID.
        """
        message_id = next(self.message_counter)
        self.messages.append({
            'id': message_id,
            'sender': sender,
            'date': post_date,
            'subject': subject
        })
        return message_id

    def save_message(self, message):
        """
        Adds a formatted message to the messages list.
        """
        self.messages.append(message)

    def list_users(self):
        """
        Returns a list of usernames currently on the bulletin board.
        """
        return list(self.users.keys())

    def get_message_content(self, message_id):
        """
        Finds and returns the content of a message with the given ID.
        """
        for message in self.messages:
            if message['id'] == message_id:
                return f"{message['sender']} on {message['date']}: {message['subject']}"
        return None

    ### Group-related methods ###

    def list_groups(self):
        """
        Lists all the groups on the bulletin board.
        """
        return list(self.groups.keys())

    def join_group(self, user, group_id):
        """
        Adds the user to the specified group, creating the group if it doesn't exist.
        """
        if user not in self.users:
            return f"User {user} not found."
        
        # Initialize the group if it doesn’t exist
        if group_id not in self.groups:
            self.groups[group_id] = set()
        
        # Add user to the group
        self.groups[group_id].add(user)
        self.users[user]['groups'].add(group_id)
        
        return f"{user} joined group {group_id}."

    def post_to_group(self, group_id, subject, content):
        """
        Posts a message to a specific group, if the group exists.
        """
        if group_id in self.groups:
            message_id = next(self.message_counter)
            self.groups[group_id].append({
                'id': message_id,
                'subject': subject,
                'content': content
            })
            return f"Message posted to group {group_id} with ID {message_id}."
        return f"Group {group_id} not found."

    def list_group_users(self, group_id):
        """
        Returns a list of users in the specified group.
        """
        if group_id in self.groups:
            return list(self.groups[group_id])
        return []

    def leave_group(self, user, group_id):
        """
        Removes a user from a specified group.
        """
        if group_id in self.groups and user in self.groups[group_id]:
            self.groups[group_id].remove(user)
            self.users[user]['groups'].remove(group_id)
            if not self.groups[group_id]:  # Remove group if empty
                del self.groups[group_id]
            return f"{user} left group {group_id}."
        return f"{user} is not in group {group_id}."

    def get_group_message(self, group_id, message_id):
        """
        Retrieves a specific message from a group based on its ID.
        """
        if group_id in self.groups:
            for message in self.groups[group_id]:
                if message['id'] == message_id:
                    return f"{message['subject']}: {message['content']}"
        return f"Message {message_id} not found in group {group_id}."
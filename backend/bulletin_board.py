import itertools

class BulletinBoard:
    def __init__(self):
        self.users = {}  # Store users in a dictionary for quick access
        self.messages = []  # List to store public messages
        self.groups = {}  # Dictionary to store groups with members and messages
        self.message_counter = itertools.count(1)  # To assign unique message IDs

    def add_user(self, user):
        """Adds a new user to the bulletin board if they are not already present."""
        if user not in self.users:
            self.users[user] = {'groups': set()}
            return f"{user} added successfully."
        return f"{user} is already a member."

    def remove_user(self, user):
        """Removes a user from the bulletin board and any groups they belong to."""
        if user in self.users:
            # Remove user from all groups they belong to
            for group in self.users[user]['groups']:
                self.groups[group]['members'].remove(user)
                if not self.groups[group]['members']:  # Remove group if empty
                    del self.groups[group]
            del self.users[user]  # Finally, remove the user from the board
            return f"{user} removed successfully."
        return f"{user} is not found."

    def add_post(self, sender, post_date, subject, content):
        """Creates a new message with a unique ID and saves it."""
        message_id = next(self.message_counter)
        message = {
            'id': message_id,
            'sender': sender,
            'date': post_date,
            'subject': subject,
            'content': content
        }
        self.messages.append(message)  # Save the message directly here
        return message_id

    def list_users(self):
        """Returns a list of usernames currently on the bulletin board."""
        return list(self.users.keys())

    def get_message_content(self, message_id):
        """Finds and returns the content of a message with the given ID."""
        for message in self.messages:
            if message['id'] == message_id:
                return f"{message['sender']} on {message['date']}: {message['subject']}"
        return None
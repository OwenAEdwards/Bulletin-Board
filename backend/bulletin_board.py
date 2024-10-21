class BulletinBoard:
    def __init__(self):
        self.users = {}
        self.messages = []

    def add_user(self, user):
        # Add user logic
        pass

    def remove_user(self, user):
        # Remove user logic
        pass

    def post_message(self, message):
        # Post message logic
        pass

    def get_last_messages(self, count=2):
        # Get last count messages
        return self.messages[-count:]

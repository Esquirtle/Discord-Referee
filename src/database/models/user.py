class User:
    def __init__(self, user_id, username, email, language='en'):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.language = language
        self.stats = {}

    def update_stats(self, stat_name, value):
        self.stats[stat_name] = value

    def get_stats(self):
        return self.stats

    def __repr__(self):
        return f"<User {self.username} (ID: {self.user_id})>"
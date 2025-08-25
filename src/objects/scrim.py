class Scrim:
    def __init__(self, match_name: str, match_code: str, owner : str):
        self.match_name = match_name
        self.match_code = match_code
        self.owner = owner
        self.id = f"{owner}-{match_code}"
        self.channel = None

    def set_channel(self, channel):
        self.channel = channel
    def get_match_name(self):
        return self.match_name
    def __str__(self):
        return f"Scrim: {self.match_name} ({self.match_code}) {self.owner}"
    def __repr__(self):
        return f"Scrim(match_name={self.match_name}, match_code={self.match_code}, owner={self.owner})"

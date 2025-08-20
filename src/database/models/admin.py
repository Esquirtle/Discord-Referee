"""
Modelo Admin para Discord Referee Bot.
"""
from typing import Optional

class Admin:
    def __init__(self, id: int, discord_id: int, permissions: str = "basic"):
        self.id = id
        self.discord_id = discord_id
        self.permissions = permissions

    def __repr__(self):
        return f"<Admin {self.discord_id} perms={self.permissions}>"

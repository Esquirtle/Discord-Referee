"""
Modelo Player para Discord Referee Bot.
"""
from typing import Optional

class Player:
    def __init__(self, id: int, discord_id: int, name: str, team_id: Optional[int] = None, stats: Optional[dict] = None):
        self.id = id
        self.discord_id = discord_id
        self.name = name
        self.team_id = team_id
        self.stats = stats or {}

    def __repr__(self):
        return f"<Player {self.name} (Discord: {self.discord_id})>"

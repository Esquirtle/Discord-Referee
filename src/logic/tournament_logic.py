from src.database.db_manager import DatabaseManager
from database.models.tournament import Tournament
from database.models.team import Team

class TournamentLogic:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    async def create_tournament(self, name: str, teams: list, rules: str):
        tournament = Tournament(name=name, rules=rules)
        await self.db_manager.save_tournament(tournament)
        for team in teams:
            await self.db_manager.add_team_to_tournament(tournament.id, team.id)

    async def get_tournament(self, tournament_id: int):
        return await self.db_manager.get_tournament(tournament_id)

    async def list_tournaments(self):
        return await self.db_manager.get_all_tournaments()

    async def join_tournament(self, tournament_id: int, team_id: int):
        tournament = await self.get_tournament(tournament_id)
        if tournament:
            await self.db_manager.add_team_to_tournament(tournament_id, team_id)

    async def start_tournament(self, tournament_id: int):
        tournament = await self.get_tournament(tournament_id)
        if tournament and not tournament.is_started:
            tournament.is_started = True
            await self.db_manager.update_tournament(tournament)

    async def end_tournament(self, tournament_id: int):
        tournament = await self.get_tournament(tournament_id)
        if tournament and tournament.is_started:
            tournament.is_started = False
            await self.db_manager.update_tournament(tournament)

    async def get_tournament_statistics(self, tournament_id: int):
        return await self.db_manager.get_tournament_statistics(tournament_id)
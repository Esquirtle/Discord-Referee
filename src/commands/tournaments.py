from discord.ext import commands
from database.manager import DatabaseManager
from logic.tournament_logic import TournamentLogic

class TournamentCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, db_manager: DatabaseManager):
        self.bot = bot
        self.db_manager = db_manager
        self.tournament_logic = TournamentLogic(db_manager)

    @commands.command(name='create_tournament')
    async def create_tournament(self, ctx, name: str, max_teams: int):
        """Create a new tournament."""
        tournament = await self.tournament_logic.create_tournament(name, max_teams)
        await ctx.send(f"Tournament '{tournament.name}' created with ID: {tournament.id}")

    @commands.command(name='join_tournament')
    async def join_tournament(self, ctx, tournament_id: int):
        """Join an existing tournament."""
        result = await self.tournament_logic.join_tournament(ctx.author.id, tournament_id)
        if result:
            await ctx.send(f"You have joined the tournament with ID: {tournament_id}")
        else:
            await ctx.send(f"Failed to join tournament with ID: {tournament_id}")

    @commands.command(name='list_tournaments')
    async def list_tournaments(self, ctx):
        """List all tournaments."""
        tournaments = await self.tournament_logic.get_all_tournaments()
        if tournaments:
            tournament_list = "\n".join([f"{t.id}: {t.name}" for t in tournaments])
            await ctx.send(f"Current tournaments:\n{tournament_list}")
        else:
            await ctx.send("No tournaments available.")

    @commands.command(name='tournament_stats')
    async def tournament_stats(self, ctx, tournament_id: int):
        """Get statistics for a specific tournament."""
        stats = await self.tournament_logic.get_tournament_stats(tournament_id)
        await ctx.send(f"Statistics for tournament ID {tournament_id}: {stats}")

def setup(bot: commands.Bot, db_manager: DatabaseManager):
    bot.add_cog(TournamentCommands(bot, db_manager))
import discord
from discord.ext import commands
from src.database.db_manager import DatabaseManager

class TeamCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, db_manager: DatabaseManager):
        self.bot = bot
        self.db_manager = db_manager

    @commands.command(name='create_team')
    async def create_team(self, ctx, team_name: str):
        # Logic to create a team in the database
        await ctx.send(f'Team "{team_name}" has been created!')

    @commands.command(name='join_team')
    async def join_team(self, ctx, team_name: str):
        # Logic to join a team in the database
        await ctx.send(f'You have joined the team "{team_name}".')

    @commands.command(name='list_teams')
    async def list_teams(self, ctx):
        # Logic to list all teams from the database
        teams = await self.db_manager.get_all_teams()
        await ctx.send(f'Available teams: {", ".join(teams)}')

    @commands.command(name='team_info')
    async def team_info(self, ctx, team_name: str):
        # Logic to get information about a specific team
        team_info = await self.db_manager.get_team_info(team_name)
        await ctx.send(f'Team Info: {team_info}')

def setup(bot: commands.Bot, db_manager: DatabaseManager):
    bot.add_cog(TeamCommands(bot, db_manager))
import discord
from discord.ext import commands
from src.database.manager import DatabaseManager
from src.logic.match_logic import MatchLogic

class MatchCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, db_manager: DatabaseManager):
        self.bot = bot
        self.db_manager = db_manager
        self.match_logic = MatchLogic(db_manager)

    @commands.command(name='create_match')
    async def create_match(self, ctx, team1: str, team2: str):
        match = await self.match_logic.create_match(team1, team2)
        await ctx.send(f'Match created between {team1} and {team2}. Match ID: {match.id}')

    @commands.command(name='join_match')
    async def join_match(self, ctx, match_id: int):
        result = await self.match_logic.join_match(ctx.author.id, match_id)
        await ctx.send(result)

    @commands.command(name='ongoing_matches')
    async def ongoing_matches(self, ctx):
        matches = await self.match_logic.get_ongoing_matches()
        if matches:
            await ctx.send(f'Ongoing matches: {", ".join([str(match.id) for match in matches])}')
        else:
            await ctx.send('No ongoing matches at the moment.')

def setup(bot: commands.Bot, db_manager: DatabaseManager):
    bot.add_cog(MatchCommands(bot, db_manager))
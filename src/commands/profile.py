import discord
from discord.ext import commands
from src.database.db_manager import DatabaseManager

class ProfileCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, db_manager: DatabaseManager):
        self.bot = bot
        self.db_manager = db_manager

    @commands.command(name='profile')
    async def view_profile(self, ctx):
        user_id = ctx.author.id
        profile_data = self.db_manager.get_user_profile(user_id)
        
        if profile_data:
            await ctx.send(f"**Profile for {ctx.author.name}:**\n"
                           f"Username: {profile_data['username']}\n"
                           f"Team: {profile_data['team']}\n"
                           f"Matches Played: {profile_data['matches_played']}\n"
                           f"Statistics: {profile_data['statistics']}")
        else:
            await ctx.send("Profile not found. Please register using the `!register` command.")

    @commands.command(name='edit_profile')
    async def edit_profile(self, ctx, *, new_username: str):
        user_id = ctx.author.id
        success = self.db_manager.update_user_profile(user_id, new_username)
        
        if success:
            await ctx.send(f"Your profile has been updated to: {new_username}")
        else:
            await ctx.send("There was an error updating your profile. Please try again.")

def setup(bot: commands.Bot, db_manager: DatabaseManager):
    bot.add_cog(ProfileCommands(bot, db_manager))
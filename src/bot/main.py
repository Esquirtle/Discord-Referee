import sys
import os
import discord
from discord.ext import commands

# Ensure the src directory is in sys.path for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import Config
from database.manager import DatabaseManager
from src.console.c_manager import ConsoleManager
from guild import GuildObject
class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        self.config = Config()
        super().__init__(command_prefix=self.config.getCommandPrefix(), intents=intents)

        self.db_manager = DatabaseManager(db_path=self.config.getDatabaseUrl())
        self.connected_guilds = []  # Se llenará en on_ready
        self.console = None
        self.guild_object = GuildObject()
        self.load_commands()
    def load_commands(self):
        # Load command modules here
        pass
    def get_guild(self):
        return self.guilds
    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print(f'Connected to {len(self.guilds)} guilds.')
        print(f'Guilds: {self.get_guild()}')
        # Llenar la lista de guilds conectados
        self.connected_guilds.clear()
        self.connected_guilds.extend(list(self.guilds))
        if not self.console:
            self.console = ConsoleManager(bot=self, connected_guilds=self.connected_guilds)
            self.console.start()

def main():
    bot = DiscordBot()
    bot.run(bot.config.getToken())

if __name__ == "__main__":
    main()
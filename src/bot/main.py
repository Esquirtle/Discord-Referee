import sys
import os
import discord
from discord.ext import commands

# Ensure the src directory is in sys.path for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import Config
from database.db_manager import DatabaseManager
from console.c_manager import ConsoleManager
from guild import GuildObject
class DiscordBot(commands.Bot):
    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        self.config = Config()
        super().__init__(command_prefix=self.config.getCommandPrefix(), intents=intents)
        self.guild_object = None
        self.db_manager = DatabaseManager()
        self.connected_guilds = []  # Se llenará en on_ready
        self.console = None
        self.guild_object = None
    # No llamar aquí, se llamará en on_ready
    async def load_commands(self):
        # Cargar automáticamente todos los módulos de src/commands excepto __init__.py
        import os
        commands_dir = os.path.join(os.path.dirname(__file__), '..', 'commands')
        for filename in os.listdir(commands_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = f"commands.{filename[:-3]}"
                try:
                    await self.load_extension(module_name)
                    print(f"[INFO] Comando cargado: {module_name}")
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar {module_name}: {e}")
    def set_guild_object(self, guild_object):
        self.guild_object = guild_object
    def get_guild(self):
        return self.guilds
    async def on_ready(self):
        await self.load_commands()
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
import asyncio
import sys
import os
import threading
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
        self.guild_object = None
        self.console_manager = None
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
    def get_guild_id(self):
        guild = self.guild_object.get_id()
        return guild
    async def on_ready(self):
        await self.load_commands()
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print(f'Connected to {len(self.guilds)} guilds.')
        # Llenar la lista de guilds conectados
        self.connected_guilds.clear()
        self.connected_guilds.extend(list(self.guilds))
        if not self.guild_object:
            self.guild_object = GuildObject(bot=self)
        # Por ejemplo, asigna el primer guild conectado
        if self.guilds:
            self.guild_object.set_discord_guild(self.guilds[3])
    #funcion para enviar mensajes
    async def send_embed(self, channel_id, embed, view):
        channel = self.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed, view=view)
    #funcion para crear categorias
    #funcion para crear canal en categoria
    async def create_channel_in(self, category_id, name, **kwargs):
        category = self.ctx.category_manager.get_category_by_id(category_id)
        if not category:
            raise ValueError("Category not found")
        return await self.ctx.create_channel(name, category=category, **kwargs)

def main():
    bot = DiscordBot()
    # Inicia el bot en el hilo principal
    threading.Thread(target=bot.run, args=(bot.config.getToken(),), daemon=True).start()
    # Espera a que el bot esté listo y tenga guilds conectados
    import time
    while not bot.connected_guilds:
        time.sleep(1)
    # Inicia la consola en un hilo separado
    console = ConsoleManager(bot, bot.connected_guilds)
    console.start()
    # Mantén el main thread vivo
    console.join()
if __name__ == "__main__":
    main()
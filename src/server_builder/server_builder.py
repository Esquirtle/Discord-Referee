import discord
from factory_panel.panel_manager import PanelManager
from factory_cac.cac_factory import CaCFactory
from languages.lang_manager import LanguageManager
from discord.ext import commands
class ServerBuilder(commands.Cog):
    def __init__(self, lang_manager : LanguageManager, bot):
        self.panel_manager = PanelManager(lang_manager, panels_dir="src/factory_panel/json_panels")
        self.bot = bot
        self.lang_manager = lang_manager
        self.cac_factory = CaCFactory(bot, lang_manager)

    async def build_server(self, guild):
        # Aquí se construiría el servidor utilizando self.panel_manager y self.cac_factory
        print("Building server with the following configuration:")
        print(f"Panel Manager: {self.panel_manager}")
        print(f"CaC Factory: {self.cac_factory}")
        await self.cac_factory.setup(guild)
        # Ejemplo de cómo podrías usar el panel_manager para cargar un panel
    
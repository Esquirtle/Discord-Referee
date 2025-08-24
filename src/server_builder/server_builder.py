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
        # Primero crea la estructura de canales/categorías
        await self.cac_factory.setup(guild)
        # Luego obtiene los mensajes a enviar
        panel_messages = self.panel_manager.get_all_panel_messages(self.cac_factory.channel_manager)
        for channel, embed, view in panel_messages:
            await channel.send(embed=embed, view=view)
            print(f"[ServerBuilder] Enviado panel a canal '{channel.name}'")

    def check_cac_factory(self):
        return self.cac_factory is not None
    def check_panel_manager(self):
        return self.panel_manager is not None
    def __repr__(self):
        return (f" \n"
                f"<ServerBuilder \n"
                f" lang_manager={self.lang_manager.lang_code},\n"
                f" panel_manager={self.check_panel_manager()},\n"
                f" cac_factory={self.check_cac_factory()}>")
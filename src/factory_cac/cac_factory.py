from .channel_manager import ChannelManager
from .category_manager import CategoryManager
from languages.lang_manager import LanguageManager
import discord
def panel_key_to_channel_key(panel_key):
    """
    Convierte claves de panel como 'register_panel' a claves de canal como 'register.panel'
    """
    return panel_key.replace("_panel", ".panel")

class CaCFactory():
    def __init__(self, bot, lang_manager, channel_manager=None, category_manager=None):
        self.bot = bot
        self.guild = None
        self.lang_manager = lang_manager
        self.channel_manager = channel_manager or ChannelManager(self.bot, lang_manager=self.lang_manager)
        self.category_manager = category_manager or CategoryManager(self.bot, lang_manager=self.lang_manager)
    print(f"CaCFactory initialized for guild:")
    def set_guild(self, guild, bot):
        self.guild = guild
        self.bot = bot
        self.channel_manager = ChannelManager(self.bot, lang_manager=self.lang_manager)
        self.category_manager = CategoryManager(self.bot, lang_manager=self.lang_manager)
    def get_guild(self):
        return self.guild
    def set_channel_manager(self, channel_manager):
        self.channel_manager = channel_manager
    def get_channel_manager(self):
        return self.channel_manager
    def set_category_manager(self, category_manager):
        self.category_manager = category_manager
    def get_category_manager(self):
        return self.category_manager
    def create_channel(self, name, **kwargs):
        return self.channel_manager.create_channel(name, **kwargs)
    async def send_embed(self, embed, view, modal, channel):
        await channel.send(embed=embed, view=view, modal=modal)
    async def nuke_guild(self):
        """
        Elimina todos los canales y categorías del servidor Discord.
        """
        await self.channel_manager.delete_all_channels()
        await self.category_manager.delete_all_categories()
    async def setup(self, discord_guild):
        """
        Crea las categorías y canales en el servidor Discord usando la configuración del idioma.
        :param discord_guild: Objeto discord.Guild real
        """
        server_config = self.lang_manager.translations.get("ServerConfig", {})
        categories_dict = server_config.get("categories", {})
        channels_dict = server_config.get("channels", {})

        # Crear categorías y guardar sus ids
        category_ids = {}
        print("[CaCFactory] Creando categorías:")
        for cat_key, cat_name in categories_dict.items():
            print(f"  Creando categoría '{cat_key}': '{cat_name}' ...")
            discord_category = await self.category_manager.create_category(cat_key, cat_name, guild=discord_guild)
            print(f"    -> ID Discord: {discord_category.id}")
            category_ids[cat_key] = discord_category.id

        # Crear canales y asociarlos a la categoría correspondiente si aplica
        print("[CaCFactory] Creando canales:")
        for chan_key, chan_name in channels_dict.items():
            if "." in chan_key:
                cat_key = chan_key.split(".")[0]
                category_id = category_ids.get(cat_key)
            else:
                category_id = None
            print(f"  Creando canal '{chan_key}': '{chan_name}' en categoría ID: {category_id}")
            discord_channel = await self.channel_manager.create_channel(chan_key, chan_name, category_id=category_id, guild=discord_guild)
            print(f"    -> ID Discord: {discord_channel.id}")

    def __str__(self):
        return (
            f"CaCFactory\n"
            f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
            f"  guild={self.guild},\n"
            f"  channel_manager={self.channel_manager},\n"
            f"  category_manager={self.category_manager},\n"
            f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        )
    
    # Channel operations
    async def create_channel(self, name, **kwargs):
        return await self.channel_manager.create_channel(name, **kwargs)

    async def edit_channel(self, channel, **kwargs):
        return await self.channel_manager.edit_channel(channel, **kwargs)
    # cac_factory.py
    async def send_panels_to_channels(self, panel_manager):
        """
        Envía los embeds generados por panel_manager a los canales correspondientes.
        """
        panels = panel_manager.build_all_panels()
        for panel_key, panel in panels.items():
            channel_key = panel_key_to_channel_key(panel_key)
            channel = self.channel_manager.get_channel_by_key(channel_key)
            if channel:
                embed = panel.get("embed")
                view = panel.get("buttons")
                await channel.send(embed=embed, view=view)
                print(f"[CaCFactory] Enviado panel '{panel_key}' a canal '{channel.name}'")
            else:
                print(f"[CaCFactory] Canal para panel '{panel_key}' no encontrado.")

    # Category operations
    async def create_category(self, name, **kwargs):
        return await self.category_manager.create_category(name, **kwargs)

    async def edit_category(self, category, **kwargs):
        return await self.category_manager.edit_category(category, **kwargs)

    async def delete_category(self, category):
        return await self.category_manager.delete_category(category)

    # Utilities

    def get_channel_by_name(self, name):
        return self.channel_manager.get_channel_by_name(name)

    def get_channel_by_id(self, channel_id):
        return self.channel_manager.get_channel_by_id(channel_id)

    def list_channels(self):
        return self.channel_manager.list_channels()

    def list_text_channels(self):
        return self.channel_manager.list_text_channels()

    def list_voice_channels(self):
        return self.channel_manager.list_voice_channels()

    def list_channels_in_category(self, category_id):
        return self.channel_manager.list_channels_in_category(category_id)

    def get_category_by_name(self, name):
        return self.category_manager.get_category_by_name(name)


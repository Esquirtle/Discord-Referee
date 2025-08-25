import discord
from languages.lang_manager import LanguageManager
from factory_cac.cac_factory import CaCFactory
from factory_panel.embeds.embed_gen import EmbedGenerator
from server_builder.server_builder import ServerBuilder
class GuildObject:
    def __init__(self, bot, discord_guild : discord.Guild = None, lang_code='eng'):
        self.bot = bot
        self.discord_guild = discord_guild  # Objeto discord.Guild real
        self.id = discord_guild.id if discord_guild else None
        self.name = discord_guild.name if discord_guild else None
        self.lang_manager = LanguageManager(lang_code=lang_code)
        self.server_builder = ServerBuilder(self.lang_manager, bot)
        self.embed_gen = None  # Se puede setear después si es necesario
        self.version = None
        self.config = None
    async def clear_data_(self):
        for channel in self.discord_guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.delete()
        for category in self.discord_guild.categories:
            if isinstance(category, discord.CategoryChannel):
                await category.delete()
        for voice in self.discord_guild.voice_channels:
            await voice.delete()

    def set_discord_guild(self, discord_guild):
        self.discord_guild = discord_guild
        self.id = discord_guild.id
        self.name = discord_guild.name
    async def setup_referee(self):
        # Lógica para configurar el referee
        await self.server_builder.build_server(self.discord_guild)
        pass
    def get_discord_guild(self):
        return self.discord_guild

    def __str__(self):
        return (
            f"GuildObject \n"
            f"  id={self.id},\n"
            f"  name={self.name},\n"
            f"  version={self.version},\n"
            f"  config={self.config},\n"
            f"  discord_guild={self.discord_guild},\n"

        )
    def get_id(self) -> int:
        return self.id
    def get_name(self):
        return self.name
    def get_config(self):
        return self.config
    def get_cac_factory(self):
        return self.cac_factory
    def get_lang_manager(self):
        return self.lang_manager
    def set_cac_factory(self, cac_factory):
        self.cac_factory = cac_factory
    def set_embed_gen(self, embed_gen):
        self.embed_gen = embed_gen
    def set_version(self, version):
        self.version = version
    def set_config(self, config):
        self.config = config
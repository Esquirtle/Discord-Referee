from languages.lang_manager import LanguageManager
from factory_cac.cac_factory import CaCFactory
from factory_panel.embeds.embed_gen import EmbedGenerator
from server_builder.server_builder import ServerBuilder

class GuildObject:
    def __init__(self, bot):
        self.bot = bot
        self.id = None
        self.name = None
        self.members = []
        self.channels = []
        self.categories = []
        self.roles = []
        self.version = None
        self.config = None
        self.lang_manager : LanguageManager = LanguageManager(lang_code='eng')
        self.server_builder : ServerBuilder = ServerBuilder(self.lang_manager, self.bot)

    def __str__(self):
        return (
            f"GuildObject\n"
            f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n"
            f"  id={self.id},\n"
            f"  name={self.name},\n"
            f"  version={self.version},\n"
            f"  config={self.config},\n"
            f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        )
    def get_id(self) -> int:
        return self.id
    def get_name(self) -> str:
        return self.name
    def get_members(self) -> list:
        return self.members
    def get_channels(self) -> list:
        return self.channels
    def get_categories(self) -> list:
        return self.categories
    def get_roles(self) -> list:
        return self.roles
    def get_config(self) -> dict:
        return self.config
    def get_cac_factory(self) -> CaCFactory:
        return self.cac_factory
    def get_lang_manager(self) -> LanguageManager:
        return self.lang_manager
    def set_cac_factory(self, cac_factory: CaCFactory):
        self.cac_factory = cac_factory
    def set_embed_gen(self, embed_gen: EmbedGenerator):
        self.embed_gen = embed_gen
    def set_id(self, guild_id):
        self.id = guild_id
    def set_name(self, guild_name):
        self.name = guild_name
    def add_member(self, member):
        self.members.append(member)
    def remove_member(self, member):
        self.members.remove(member)
    def add_category(self, category):
        self.categories.append(category)
    def remove_category(self, category):
        self.categories.remove(category)
    def add_channel(self, channel):
        self.channels.append(channel)
    def remove_channel(self, channel):
        self.channels.remove(channel)
    def add_role(self, role):
        self.roles.append(role)
    def remove_role(self, role):
        self.roles.remove(role)
    def set_version(self, version):
        self.version = version
    def set_config(self, config):
        self.config = config

    def set_channels(self, channels):
        self.channels = list(channels)
    def set_members(self, members):
        self.members = list(members)
    def set_roles(self, roles):
        self.roles = list(roles)
    def set_categories(self, categories):
        self.categories = list(categories)
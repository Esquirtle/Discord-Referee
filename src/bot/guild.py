from languages.lang_manager import LanguageManager


class GuildObject:
    def __init__(self):
        self.id = None
        self.name = None
        self.members = []
        self.channels = []
        self.categories = []
        self.roles = []
        self.version = None
        self.config = None
        self.lang_manager = LanguageManager()
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
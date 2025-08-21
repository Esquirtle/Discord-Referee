from .channel_manager import ChannelManager
from .category_manager import CategoryManager
from languages.lang_manager import LanguageManager
class CaCFactory:
    def __init__(self, bot, lang_manager : LanguageManager):
        self.bot = bot
        self.guild = None
        self.lang_manager = lang_manager
        self.channel_manager = ChannelManager(self.bot, lang_manager=self.lang_manager)
        self.category_manager = CategoryManager(self.bot, lang_manager=self.lang_manager)
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

    async def setup(self):
        await self.channel_manager.load_channels_from_lang()
        await self.category_manager.load_categories_from_lang()
        categories = self.category_manager.get_categories()
        for category in categories:
            category.channels = self.bot.create_category(category.name)

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

    async def delete_channel(self, channel):
        return await self.channel_manager.delete_channel(channel)

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


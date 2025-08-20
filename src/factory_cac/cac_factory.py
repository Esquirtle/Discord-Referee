from channel_manager import ChannelManager
from category_manager import CategoryManager

class CaCFactory:
    def __init__(self, guild):
        self.guild = guild
        self.channel_manager = ChannelManager(guild)
        self.category_manager = CategoryManager(guild)

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

class ChannelManager:
    def __init__(self, guild):
        self.guild = guild

    async def create_channel(self, name, category_id=None, **kwargs):
        category = None
        if category_id is not None:
            category = self.guild.get_channel(category_id)
            if category is None or not getattr(category, "is_category", lambda: False)():
                # Fallback: buscar en guild.categories
                for cat in getattr(self.guild, "categories", []):
                    if cat.id == category_id:
                        category = cat
                        break
        return await self.guild.create_text_channel(name, category=category, **kwargs)

    async def edit_channel(self, channel, **kwargs):
        await channel.edit(**kwargs)
        return channel

    async def delete_channel(self, channel):
        await channel.delete()
        return True

    def get_channel_by_name(self, name):
        for channel in self.guild.channels:
            if channel.name == name:
                return channel
        return None

    def get_channel_by_id(self, channel_id):
        for channel in self.guild.channels:
            if channel.id == channel_id:
                return channel
        return None

    def list_channels(self):
        return list(self.guild.channels)

    def list_text_channels(self):
        return [ch for ch in self.guild.channels if getattr(ch, "type", None) and str(ch.type) == "text"]

    def list_voice_channels(self):
        return [ch for ch in self.guild.channels if getattr(ch, "type", None) and str(ch.type) == "voice"]

    def list_channels_in_category(self, category_id):
        return [ch for ch in self.guild.channels if getattr(ch, "category_id", None) == category_id]

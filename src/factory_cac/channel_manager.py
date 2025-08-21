import discord
class ChannelManager():
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild

    async def create_channel(self, name, **kwargs):
        # Obtener el objeto Guild desde el bot si self.guild es un id
        guild = self.guild
        if isinstance(guild, int):
            # Buscar el objeto Guild real usando el bot
            guild = self.bot.get_guild(guild)
        if guild is None:
            raise ValueError("ChannelManager: 'guild' is None or invalid. Cannot create channel.")
        return await guild.create_text_channel(name, **kwargs)

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

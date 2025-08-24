import discord

from languages.lang_manager import LanguageManager
class Channel:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.category_id = None
    def __repr__(self):
        return f"<Channel name={self.name} id={self.id} category_id={self.category_id}>"
class ChannelManager:
    def __init__(self, bot, lang_manager):
        self.bot = bot
        self.lang_manager = lang_manager
        self.channels = {}

    def __repr__(self):
        return f"<ChannelManager bot={self.bot} lang_manager={self.lang_manager}>"

    def load_channels_from_lang(self):
        """
        Carga los canales desde el archivo de idioma y crea objetos Channel.
        """
        channels_dict = self.lang_manager.translations.get("channels", {})
        for key, name in channels_dict.items():
            self.channels[key] = Channel(name=name)

    async def create_channel(self, key, name, category_id=None, guild=None, **kwargs):
        category = None
        if category_id:
            category = discord.utils.get(guild.categories, id=category_id)
        discord_channel = await guild.create_text_channel(name, category=category, **kwargs)
        self.channels[key] = discord_channel  # Guarda el canal real de Discord
        return discord_channel

    def get_channel_by_key(self, key):
        return self.channels.get(key)

    async def edit_channel(self, channel, **kwargs):
        await channel.edit(**kwargs)
        return channel

    async def delete_channel(self, channel):
        await channel.delete()
        return True

    def get_channel_by_name(self, name):
        return self.channels.get(name)

    def get_channel_by_id(self, channel_id):
        for channel in self.channels.values():
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

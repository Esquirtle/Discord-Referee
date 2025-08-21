import discord

from languages.lang_manager import LanguageManager
class ChannelManager:
    def __init__(self, bot, lang_manager: LanguageManager):
        self.bot = bot
        self.lang_manager = lang_manager
        self.channels: dict[str, Channel] = {}

    def __repr__(self):
        return f"<ChannelManager bot={self.bot} lang_manager={self.lang_manager}>"

    def load_channels_from_lang(self):
        """
        Carga los canales desde el archivo de idioma y crea objetos Channel.
        """
        channels_dict = self.lang_manager.translations.get("channels", {})
        for key, name in channels_dict.items():
            self.channels[key] = Channel(name=name)

    async def create_channel(self, key, category_id=None, **kwargs):
        """
        Crea el canal en Discord usando el nombre del idioma y guarda la id.
        """
        channel_obj = self.channels.get(key)
        if not channel_obj:
            raise ValueError(f"Channel key '{key}' not found.")
        guild = kwargs.pop("guild", None) or self.bot.guilds[0]
        discord_channel = await guild.create_text_channel(channel_obj.name, category_id=category_id, **kwargs)
        channel_obj.id = discord_channel.id
        channel_obj.category_id = category_id
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
class Channel:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.category_id = None
    def __repr__(self):
        return f"<Channel name={self.name} id={self.id} category_id={self.category_id}>"
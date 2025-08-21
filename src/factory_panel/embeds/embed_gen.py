import discord

class EmbedGenerator:
    def __init__(self, lang_manager):
        self.lang_manager = lang_manager

    def from_config(self, config):
        embed = discord.Embed(
            title=self.lang_manager.get_text(config.get("title", "")),
            description=self.lang_manager.get_text(config.get("description", "")),
            color=discord.Color(config.get("color", 0x3498db))
        )
        for field in config.get("fields", []):
            embed.add_field(
                name=self.lang_manager.get_text(field.get("name", "")),
                value=self.lang_manager.get_text(field.get("value", "")),
                inline=field.get("inline", False)
            )
        if "footer" in config:
            embed.set_footer(text=self.lang_manager.get_text(config["footer"]))
        if "thumbnail" in config:
            embed.set_thumbnail(url=config["thumbnail"])
        if "image" in config:
            embed.set_image(url=config["image"])
        return embed

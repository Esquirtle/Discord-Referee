import discord
class EmbedGenerator:
    def __init__(self, lang_manager):
        self.lang_manager = lang_manager
        self.embeds : discord.Embed = {}
        self.load_embeds
    def load_embeds(self, panels_dir=None):
        # Cargar los embeds desde los archivos JSON de paneles
        import os, json
        if panels_dir is None:
            # Por defecto, buscar en el directorio json_panels junto a este archivo
            panels_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'json_panels'))
        loaded = 0
        for filename in os.listdir(panels_dir):
            if filename.endswith('.json'):
                path = os.path.join(panels_dir, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    embed_config = data.get('embed')
                    if embed_config:
                        name = filename.replace('.json', '')
                        print(f"Loading embed: {name} from {filename}")
                        self.embeds[name] = EmbedObj(self.from_config(embed_config))
                        loaded += 1
        print(f"Loaded {loaded} embeds from {panels_dir}.")
    
    def from_config(self, config):
        title = self.lang_manager.get_text(config.get("title", ""))
        desc_raw = config.get("description", "")
        description = self.lang_manager.get_text(desc_raw)
        # Discord requiere que description no sea vacío
        if not description:
            description = " "
        embed = discord.Embed(
            title=title,
            description=description,
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
    def get_embed(self, name):
        return self.embeds.get(name)
class EmbedObj:
    def __init__(self, embed: discord.Embed):
        self.embed : discord.Embed = embed
        self.name = embed.title
    def __str__(self):
        return f"EmbedObj(name={self.name})"
    def to_dict(self):
        return {
            "name": self.name,
            "embed": self.embed.to_dict()
        }
from languages.lang_manager import LanguageManager


class CategoryManager:
    def __init__(self, bot, lang_manager: LanguageManager):
        self.bot = bot
        self.lang_manager = lang_manager
        self.categories: dict[str, Category] = {}

    def __repr__(self):
        return f"<CategoryManager bot={self.bot} lang_manager={self.lang_manager}>"

    def load_categories_from_lang(self):
        """
        Carga las categorías desde el archivo de idioma y crea objetos Category.
        """
        categories_dict = self.lang_manager.get_categories()
        for key, name in categories_dict.items():
            self.categories[key] = Category(name=name)

    async def create_category(self, key, **kwargs):
        """
        Crea la categoría en Discord usando el nombre del idioma y guarda la id.
        """
        category_obj = self.categories.get(key)
        if not category_obj:
            raise ValueError(f"Category key '{key}' not found.")
        guild = kwargs.pop("guild", None) or self.bot.guilds[0]
        discord_category = await guild.create_category(category_obj.name, **kwargs)
        category_obj.id = discord_category.id
        return discord_category

    def get_category_by_key(self, key):
        return self.categories.get(key)

    async def edit_category(self, category, **kwargs):
        await category.edit(**kwargs)
        return category

    async def delete_category(self, category):
        await category.delete()
        return True
    def get_categories(self):
        return list(self.categories.values())

    def get_category_by_name(self, name):
        for category in self.categories.values():
            if category.name == name:
                return category
        return None
class Category:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.channels = []
    def __repr__(self):
        return f"<Category name={self.name} id={self.id}>"
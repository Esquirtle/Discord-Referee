from languages.lang_manager import LanguageManager
class Category:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.channels = []
    def __repr__(self):
        return f"<Category name={self.name} id={self.id}>"
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def set_id(self, id):
        self.id = id
    def set_name(self, name):
        self.name = name
class CategoryManager:
    def __init__(self, bot, lang_manager):
        self.bot = bot
        self.lang_manager = lang_manager
        self.categories = {}


    def __repr__(self):
        return f"<CategoryManager bot={self.bot} lang_manager={self.lang_manager}>"

    def load_categories_from_lang(self):
        """
        Carga las categorías desde el archivo de idioma y crea objetos Category.
        """
        categories_dict = self.lang_manager.get_categories()
        for key, name in categories_dict.items():
            self.categories[key] = Category(name=name)

    async def create_category(self, key, name, guild):
        """
        Crea la categoría en Discord usando el nombre del idioma y guarda la id.
        Siempre añade un objeto Category a la lista, con id y nombre.
        """
        category_obj = self.categories.get(key)
        if not category_obj:
            category_obj = Category(name=name)
        discord_category = await guild.create_category(name)
        category_obj.id = discord_category.id
        self.categories[key] = category_obj
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

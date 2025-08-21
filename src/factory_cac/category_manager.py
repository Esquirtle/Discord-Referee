from languages.lang_manager import LanguageManager


class CategoryManager:
    def __init__(self, bot, lang_manager: LanguageManager):
        self.bot = bot
        self.lang_manager = lang_manager
        self.categories : list[Category] = []
    def __repr__(self):
        return f"<CategoryManager bot={self.bot} lang_manager={self.lang_manager}>"

    async def create_category(self, name, **kwargs):
        category = await self.bot.create_category(name, **kwargs)
        self.categories[category.id] = category
        return category

    async def edit_category(self, category, **kwargs):
        await category.edit(**kwargs)
        return category

    async def delete_category(self, category):
        await category.delete()
        return True

    def get_category_by_name(self, name):
        for category in self.guild.categories:
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
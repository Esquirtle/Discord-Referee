class CategoryManager:
    def __init__(self, guild):
        self.guild = guild

    async def create_category(self, name, **kwargs):
        return await self.guild.create_category(name, **kwargs)

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

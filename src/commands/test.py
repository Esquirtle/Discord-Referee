import discord
from discord.ext import commands
from languages.lang_manager import LanguageManager
import os

class TestCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lang_manager = LanguageManager()
        # Establece el directorio de idiomas al inicializar
        locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'languages', 'locales')
        self.lang_manager.lang_dir = locales_dir

    @commands.command(name='test')
    async def test_command(self, ctx: commands.Context):
        await ctx.send('Pong!')

    @commands.command(name='test_lang_manager')
    async def test_lang_manager(self, ctx: commands.Context, lang: str = 'eng'):
        if lang not in ['eng', 'esp']:
            await ctx.send("Idioma no soportado. Usa 'eng' o 'esp'.")
            return
        self.lang_manager.lang_code = lang
        greeting = self.lang_manager.get_text('greeting')
        await ctx.send(f"LangManager test ({lang}): {greeting}")

async def setup(bot: commands.Bot):
    await bot.add_cog(TestCommands(bot))
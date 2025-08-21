import discord
from discord.ext import commands
from languages.lang_manager import LanguageManager
import os

from factory_panel.panel_manager import PanelManager

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
    @commands.command(name='test_panels')
    async def test_panels(self, ctx: commands.Context):
        panel_manager = PanelManager(self.lang_manager)
        panel = panel_manager.build_panel("example_panel")
        embed = panel.get("embed")
        modal = panel.get("modal")
        # Mapeo: custom_id del botón "ok_btn" abre el modal
        modal_map = {}
        if modal:
            modal_map["ok_btn"] = modal  # custom_id del botón que debe abrir el modal

        # Genera la view con el mapeo de modales
        view = panel_manager.button_gen.from_config(
            panel_manager.load_panel_config("example_panel").get("buttons", {}),
            button_handlers=None,
            modal_map=modal_map
        )
        await ctx.send(embed=embed, view=view)
        # Si quieres probar el modal, deberías usarlo en una interacción, no en un comando de texto

    @commands.command(name='test_register_panel')
    async def test_register_panel(self, ctx: commands.Context):
        from factory_panel.panel_manager import PanelManager
        from database.db_manager import DatabaseManager

        panel_manager = PanelManager(self.lang_manager)
        db_manager = DatabaseManager()
        guild_id = ctx.guild.id if ctx.guild else 0
        user_id = ctx.author.id

        # Callback para el submit del modal
        async def on_submit(modal, interaction):
            # Obtiene el Steam ID del primer campo del modal
            steam_id = None
            for child in modal.children:
                if hasattr(child, "value"):
                    steam_id = child.value
                    break
            if not steam_id:
                await interaction.response.send_message(
                    self.lang_manager.get_text("error_not_found"), ephemeral=True
                )
                return

            # Registrar usuario en la base de datos
            db_manager.register_user(guild_id, user_id, steam_id, user_type="player")
            await interaction.response.send_message(
                self.lang_manager.get_text("register_success"),
                ephemeral=True
            )

        # Construye el modal con el callback
        panel_config = panel_manager.load_panel_config("register_panel")
        modal = panel_manager.modal_gen.from_config(panel_config.get("modal", {}), on_submit_callback=on_submit)

        # Mapeo para que el botón abra el modal
        modal_map = {}
        if modal:
            modal_map["register_btn"] = modal

        # Genera la view con el mapeo de modales
        view = panel_manager.button_gen.from_config(
            panel_config.get("buttons", {}),
            button_handlers=None,
            modal_map=modal_map
        )
        embed = panel_manager.embed_gen.from_config(panel_config.get("embed", {}))
        await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(TestCommands(bot))
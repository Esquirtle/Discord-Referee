import discord
from discord.ext import commands
from languages.lang_manager import LanguageManager
import os
import threading
from factory_panel.panel_manager import PanelManager
from factory_cac.cac_factory import CaCFactory
from factory_panel.embeds.embed_gen import EmbedGenerator
from factory_panel.buttons.view_gen import ViewGenerator
from server_builder.server_builder import ServerBuilder

class TestCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='test')
    async def test_command(self, ctx: commands.Context):
        await ctx.send('Pong!')

    @commands.command(name='test_lang_manager')
    async def test_lang_manager(self, ctx: commands.Context, lang: str = 'eng'):
        if lang not in ['eng', 'esp']:
            await ctx.send("Idioma no soportado. Usa 'eng' o 'esp'.")
            return
        self.bot.guild_object.lang_manager.lang_code = lang
        greeting = self.bot.guild_object.lang_manager.get_text('greeting')
        await ctx.send(f"LangManager test ({lang}): {greeting}")

    @commands.command(name='test_panels')
    async def test_panels(self, ctx: commands.Context):
        panel_manager = PanelManager(self.bot.guild_object.get_lang_manager())
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
        from factory_panel.buttons.view_gen import ViewGenerator
        panel_manager = PanelManager(self.bot.guild_object.get_lang_manager())
        embed = panel_manager.embed_gen.from_config(panel_manager.load_panel_config("register_panel").get("embed", {}))
        # Usar ViewGenerator para cargar la view desde el panel y handlers centralizados
        view_gen = ViewGenerator(self.bot.guild_object.get_lang_manager())
        view = view_gen.from_panel_json("register_panel")
        await ctx.send(embed=embed, view=view)
    @commands.command(name='test_builder')
    async def test_builder(self, ctx: commands.Context):
        
        guild = ctx.guild
        cac_factory = CaCFactory(guild, self.bot)
        lang = self.bot.guild_object.get_lang_manager()
        embed_gen = EmbedGenerator(lang_manager=lang)
        self.bot.guild_object.set_cac_factory(cac_factory)
        self.bot.guild_object.set_embed_gen(embed_gen)
        embed_gen.load_embeds()
        myembed = embed_gen.get_embed("example_panel")
        #Obtener la view del embed example_panel
        view_gen = ViewGenerator(lang)
        myview = view_gen.from_panel_json("example_panel")
        if not guild:
            await ctx.send("Este comando solo se puede usar en un servidor.")
            return
        # Prueba de la fábrica CaC
        channel = await self.bot.guild_object.cac_factory.create_channel("test-channel")
        await ctx.send(f"Canal creado: {channel.name}")

        await ctx.send(embed=myembed.embed, view=myview)
    @commands.command(name='test_server_builder')
    
    async def test_server_builder(self, ctx: commands.Context):
        for channel in ctx.guild.channels:
            await channel.delete()
        lang_manager = self.bot.guild_object.get_lang_manager()
        panel_manager = PanelManager(lang_manager)
        cac_factory = CaCFactory(ctx.guild, lang_manager)
        server_builder = ServerBuilder(lang_manager, ctx.guild)
        server_builder.panel_manager = panel_manager
        server_builder.cac_factory = cac_factory
        await server_builder.build_server(ctx.guild)
    @commands.command(name='nuke')
    async def nuke(self, ctx: commands.Context):
        for channel in ctx.guild.channels:
            await channel.delete()
async def setup(bot: commands.Bot):
    await bot.add_cog(TestCommands(bot))
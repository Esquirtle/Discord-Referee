# modal_handlers.py
# Centraliza la generación y acciones de los modales para los paneles

import discord
from factory_panel.panel_manager import PanelManager
from database.db_manager import DatabaseManager
from languages.lang_manager import LanguageManager

async def handle_register_modal(interaction: discord.Interaction):
    bot = interaction.client
    guild_object = getattr(bot, 'guild_object', None)
    lang_manager = guild_object.lang_manager if guild_object else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    user_id = interaction.user.id

    panel_manager = PanelManager(lang_manager)
    panel_config = panel_manager.load_panel_config("register_panel")
    async def on_submit(modal, interaction):
        steam_id = None
        for child in modal.children:
            if hasattr(child, "value"):
                steam_id = child.value
                break
        if not steam_id:
            await interaction.response.send_message(
                lang_manager.get_text("error_not_found"), ephemeral=True
            )
            return
        db_manager.register_user(guild_id, user_id, steam_id, user_type="player")
        await interaction.response.send_message(
            lang_manager.get_text("register_success"), ephemeral=True
        )
    # Construir el modal y mostrarlo
    modal = panel_manager.modal_gen.from_config(panel_config.get("modal", {}), on_submit_callback=on_submit)
    await interaction.response.send_modal(modal)

# Mapea custom_id de modal a función handler
MODAL_ACTIONS = {
    "register_modal": handle_register_modal,
}

def get_modal_handler(custom_id):
    return MODAL_ACTIONS.get(custom_id)

# modal_handlers.py
# Centraliza la generación y acciones de los modales para los paneles

import discord
from factory_panel.panel_manager import PanelManager
from database.db_manager import DatabaseManager
from languages.lang_manager import LanguageManager

async def handle_register_submit(modal, interaction):
    lang_manager = getattr(interaction.client, 'guild_object', None)
    lang_manager = lang_manager.lang_manager if lang_manager else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    user_id = interaction.user.id

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

async def handle_modify_submit(modal, interaction):
    # Similar a register, pero actualiza el Steam ID
    lang_manager = getattr(interaction.client, 'guild_object', None)
    lang_manager = lang_manager.lang_manager if lang_manager else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    user_id = interaction.user.id

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
    db_manager.update_user_steam_id(guild_id, user_id, steam_id)
    await interaction.response.send_message(
        lang_manager.get_text("modify_success"), ephemeral=True
    )

async def handle_delete_submit(modal, interaction):
    lang_manager = getattr(interaction.client, 'guild_object', None)
    lang_manager = lang_manager.lang_manager if lang_manager else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    user_id = interaction.user.id

    db_manager.delete_user(guild_id, user_id)
    await interaction.response.send_message(
        lang_manager.get_text("delete_success"), ephemeral=True
    )

async def handle_scrim_new(modal, interaction):
    lang_manager = getattr(interaction.client, 'guild_object', None)
    lang_manager = lang_manager.lang_manager if lang_manager else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    user_id = interaction.user.id
    interaction.match_name
    # Aquí puedes manejar la lógica para el nuevo scrim
    await interaction.response.send_message(
        lang_manager.get_text("scrim_new_success"), ephemeral=True
    )

# Mapea custom_id de modal a función handler
MODAL_SUBMIT_ACTIONS = {
    "register_btn": handle_register_submit,
    "register_modify_btn": handle_modify_submit,
    "register_delete_btn": handle_delete_submit,
    "scrim_new_btn": handle_scrim_new,
}

def get_modal_submit_handler(custom_id):
    return MODAL_SUBMIT_ACTIONS.get(custom_id)
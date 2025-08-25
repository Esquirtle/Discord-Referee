# modal_handlers.py
# Centraliza la generación y acciones de los modales para los paneles

import discord
from database.db_manager import DatabaseManager
from languages.lang_manager import LanguageManager
from objects.scrim import Scrim
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
async def handle_create_scrim(modal, interaction):
    lang_manager = getattr(interaction.client, 'guild_object', None)
    lang_manager = lang_manager.lang_manager if lang_manager else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    match_code = modal.match_code
    match_name = modal.match_name
    
    # Aquí puedes manejar la lógica para crear un nuevo scrim
    await interaction.response.send_message(
        lang_manager.get_text("scrim_create_success"), ephemeral=True
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
    user_id = interaction.user.name

    # Extrae los valores de los campos del modal
    match_name = modal.children[0].value if len(modal.children) > 0 else None
    match_code = modal.children[1].value if len(modal.children) > 1 else None

    scrim = Scrim(match_name=match_name, match_code=match_code, owner=user_id)
    print(f"Nuevo scrim creado por {interaction.user}: {scrim}")
    print(f"Creando canal para scrim {scrim.id}")
    server_builder = getattr(interaction.client, 'guild_object', None)
    server_builder = server_builder.server_builder
    if server_builder:
        channel = await server_builder.create_scrim_channel(scrim)
    scrim.set_channel(channel)
    await interaction.response.send_message(
        lang_manager.get_text("scrim_new_success"), ephemeral=True
    )

# Mapea custom_id de modal a función handler
MODAL_SUBMIT_ACTIONS = {
    "register_btn": handle_register_submit,
    "register_modify_btn": handle_modify_submit,
    "register_delete_btn": handle_delete_submit,
    "scrim_create_btn": handle_scrim_new,
}

def get_modal_submit_handler(custom_id):
    return MODAL_SUBMIT_ACTIONS.get(custom_id)
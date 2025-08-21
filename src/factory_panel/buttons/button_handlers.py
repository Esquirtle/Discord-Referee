# Handler para el botón register_btn
from database.db_manager import DatabaseManager
from languages.lang_manager import LanguageManager

async def handle_register_btn(interaction: 'discord.Interaction'):
    # Obtener contexto y managers
    bot = interaction.client
    guild_object = getattr(bot, 'guild_object', None)
    lang_manager = guild_object.lang_manager if guild_object else LanguageManager()
    db_manager = DatabaseManager()
    guild_id = interaction.guild.id if interaction.guild else 0
    user_id = interaction.user.id

    # Callback para el submit del modal
    from factory_panel.panel_manager import PanelManager
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



import discord

async def handle_ok_btn(interaction: discord.Interaction):
    await interaction.response.send_message("OK button pressed!", ephemeral=True)

async def handle_cancel_btn(interaction: discord.Interaction):
    await interaction.response.send_message("Cancel button pressed!", ephemeral=True)


# Mapea custom_id a función handler
BUTTON_ACTIONS = {
    "ok_btn": handle_ok_btn,
    "cancel_btn": handle_cancel_btn,
    "register_btn": handle_register_btn,
}

def get_button_handler(custom_id):
    return BUTTON_ACTIONS.get(custom_id)

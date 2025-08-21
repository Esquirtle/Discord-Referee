import discord

class ViewGenerator:
    def __init__(self, lang_manager):
        self.lang_manager = lang_manager

    def from_config(self, config, button_handlers=None, modal_map=None):
        """
        button_handlers: dict custom_id -> callback(interaction)
        modal_map: dict custom_id -> Modal instance or callable returning Modal
        """
        buttons_config = config.get("buttons", [])
        view = discord.ui.View()
        for btn in buttons_config:
            custom_id = btn.get("custom_id", None)
            label = self.lang_manager.get_text(btn.get("label", ""))
            style = getattr(discord.ButtonStyle, btn.get("style", "primary"))
            button = discord.ui.Button(
                label=label,
                style=style,
                custom_id=custom_id
            )

            # Handler para abrir modal o ejecutar callback
            async def on_click(interaction, cid=custom_id):
                if modal_map and cid in modal_map:
                    modal = modal_map[cid]
                    if callable(modal):
                        modal = modal()
                    await interaction.response.send_modal(modal)
                elif button_handlers and cid in button_handlers:
                    await button_handlers[cid](interaction)
                else:
                    await interaction.response.send_message(f"Button {cid} pressed.", ephemeral=True)

            button.callback = on_click
            view.add_item(button)
        return view

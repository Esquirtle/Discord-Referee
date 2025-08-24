import discord

class ViewGenerator:
    def __init__(self, lang_manager):
        self.lang_manager = lang_manager
    def from_config(self, config, button_handlers=None, modal_map=None):
        import discord
        view = discord.ui.View()
        # Normaliza config a lista de botones
        if isinstance(config, dict):
            buttons = config.get("buttons", list(config.values()))
        elif isinstance(config, list):
            buttons = config
        else:
            buttons = []
    
        for btn_data in buttons:
            label = self.lang_manager.get_text(btn_data.get("label", ""))
            style = getattr(discord.ButtonStyle, btn_data.get("style", "primary"), discord.ButtonStyle.primary)
            custom_id = btn_data.get("custom_id", None)
            button = discord.ui.Button(label=label, style=style, custom_id=custom_id)
    
            async def on_click(interaction, cid=custom_id):
                if modal_map and cid in modal_map:
                    modal = modal_map[cid]
                    if callable(modal):
                        modal = modal()
                    await interaction.response.send_modal(modal)
                else:
                    await interaction.response.send_message("No modal assigned.", ephemeral=True)
    
            button.callback = on_click
            view.add_item(button)
        return view
    def fusion_modal(self, view, modal):
        self.view = view
        self.modal = modal
        view.modal = modal
        return view
    def from_panel_json(self, panel_name, panels_dir=None, button_handlers=None, modal_map=None):
        """
        Carga los botones desde el archivo JSON del panel indicado.
        """
        import os, json
        if panels_dir is None:
            panels_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'json_panels'))
        path = os.path.join(panels_dir, f"{panel_name}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Panel JSON not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            buttons_section = data.get('buttons', {})
            # Puede estar como {"buttons": [...]}, o directamente como lista
            if isinstance(buttons_section, dict):
                buttons_config = buttons_section.get('buttons', [])
            else:
                buttons_config = buttons_section
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

            # Handler para abrir modal o ejecutar acción centralizada
            from .button_handlers import get_button_handler
            async def on_click(interaction, cid=custom_id):
                if modal_map and cid in modal_map:
                    modal = modal_map[cid]
                    if callable(modal):
                        modal = modal()
                    await interaction.response.send_modal(modal)
                else:
                    handler = get_button_handler(cid)
                    if handler:
                        await handler(interaction)
                    elif button_handlers and cid in button_handlers:
                        await button_handlers[cid](interaction)
                    else:
                        await interaction.response.send_message(f"Button {cid} pressed.", ephemeral=True)
            button.callback = on_click
            view.add_item(button)
        return view

import discord

class ModalGenerator:
    def __init__(self, lang_manager):
        self.lang_manager = lang_manager

    def from_config(self, config, on_submit_callback=None):
        lang_manager = self.lang_manager
        class CustomModal(discord.ui.Modal):
            def __init__(self):
                super().__init__(title=lang_manager.get_text(config.get("title", "")))
                for field in config.get("fields", []):
                    self.add_item(
                        discord.ui.TextInput(
                            label=lang_manager.get_text(field.get("label", "")),
                            placeholder=lang_manager.get_text(field.get("placeholder", "")),
                            required=field.get("required", True),
                            style=getattr(discord.TextStyle, field.get("style", "short").upper(), discord.TextStyle.short)
                        )
                    )
            async def on_submit(self, interaction: discord.Interaction):
                if on_submit_callback:
                    await on_submit_callback(self, interaction)
                # Si no hay callback, no hace nada
        return CustomModal()

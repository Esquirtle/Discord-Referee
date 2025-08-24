import json
import os

from flask import config
from .embeds.embed_gen import EmbedGenerator
from .buttons.view_gen import ViewGenerator
from .modals.modal_gen import ModalGenerator

class PanelManager:
    def __init__(self, lang_manager, panels_dir=None):
        self.lang_manager = lang_manager
        if panels_dir is None:
            panels_dir = os.path.join(os.path.dirname(__file__), "json_panels")
        self.panels_dir = panels_dir
        self.embed_gen = EmbedGenerator(lang_manager)
        self.button_gen = ViewGenerator(lang_manager)
        self.modal_gen = ModalGenerator(lang_manager)
        self.load_panel_config
    def get_all_panel_messages(self, channel_manager, panel_key_to_channel_key=None):
        """
        Devuelve una lista de tuplas (canal, embed, view) para todos los paneles.
        :param channel_manager: manager que permite obtener los canales por clave
        :param panel_key_to_channel_key: función opcional para mapear clave de panel a clave de canal
        :return: lista de (channel, embed, view)
        """
        if panel_key_to_channel_key is None:
            def panel_key_to_channel_key(panel_key):
                return panel_key.replace('_panel', '.panel')
        panels = self.build_all_panels()
        messages = []
        for panel_key, panel in panels.items():
            channel_key = panel_key_to_channel_key(panel_key)
            channel = channel_manager.get_channel_by_key(channel_key)
            if channel:
                embed = panel.get("embed")
                view = panel.get("buttons")
                if embed:
                    messages.append((channel, embed, view))
            else:
                print(f"[PanelManager] Canal para panel '{panel_key}' no encontrado.")
        return messages
    def load_panel_config(self, panel_name):
        path = os.path.join(self.panels_dir, f"{panel_name}.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_panel(self, panel_name):
        config = self.load_panel_config(panel_name)
        embed = self.embed_gen.from_config(config.get("embed", {}))
        modals_config = config.get("modals", {})
        modal_map = {}
        for custom_id, modal_conf in modals_config.items():
            modal_map[custom_id] = self.modal_gen.from_config(modal_conf)
        buttons = config.get("buttons", {})
        view = self.button_gen.from_config(buttons, modal_map=modal_map)
        return {"embed": embed, "buttons": view, "modal_map": modal_map}

    def build_all_panels(self):
        panels = {}
        for panel_name in os.listdir(self.panels_dir):
            if panel_name.endswith(".json"):
                panel_name = panel_name[:-5]  # Remove .json extension
                panels[panel_name] = self.build_panel(panel_name)
        return panels

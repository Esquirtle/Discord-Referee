import json
import os
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

    def load_panel_config(self, panel_name):
        path = os.path.join(self.panels_dir, f"{panel_name}.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def build_panel(self, panel_name):
        config = self.load_panel_config(panel_name)
        embed = self.embed_gen.from_config(config.get("embed", {}))
        buttons = self.button_gen.from_config(config.get("buttons", {}))
        modal = None
        if "modal" in config:
            modal = self.modal_gen.from_config(config["modal"])
        return {"embed": embed, "buttons": buttons, "modal": modal}
    def build_all_panels(self):
        panels = {}
        for panel_name in os.listdir(self.panels_dir):
            if panel_name.endswith(".json"):
                panel_name = panel_name[:-5]  # Remove .json extension
                panels[panel_name] = self.build_panel(panel_name)
        return panels

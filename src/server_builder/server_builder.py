import discord
from factory_panel.panel_manager import PanelManager
from factory_cac.cac_factory import CaCFactory
class ServerBuilder:
    def __init__(self, panel_manager : PanelManager, cac_factory : CaCFactory):
        self.panel_manager = panel_manager
        self.cac_factory = cac_factory

    def build_server(self):
        # Aquí se construiría el servidor utilizando self.panel_manager y self.cac_factory
        print("Building server with the following configuration:")
        print(f"Panel Manager: {self.panel_manager}")
        print(f"CaC Factory: {self.cac_factory}")
        # Ejemplo de cómo podrías usar el panel_manager para cargar un panel
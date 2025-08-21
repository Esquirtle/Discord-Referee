import threading
from .console_utils import mostrar_servidores, seleccionar_servidor
from .setup_commands import setup_db
from bot.guild import GuildObject

class ConsoleManager(threading.Thread):
    def __init__(self, bot, connected_guilds):
        super().__init__(daemon=True)
        self.bot = bot
        self.running = True
        self.connected_guilds = connected_guilds
        self.current_guild = None
        self.guild_language = {}  # guild_id: lang_code

    def run(self):
        print("Consola de comandos iniciada. Escribe 'exit' para salir.")
        if not self.connected_guilds:
            print("No hay servidores conectados. Esperando...")
            return
        self.current_guild = seleccionar_servidor(self.connected_guilds)
        if self.current_guild is None:
            print("No hay servidores conectados. Cerrando consola...")
            return
        print(f"Servidor actual: {getattr(self.current_guild, 'name', self.current_guild)} (ID: {getattr(self.current_guild, 'id', self.current_guild)})")
        self.change_guild(self.current_guild)
        while self.running:
            try:
                command = input(f"[ {self.current_guild} ]> ").strip()
                if command.lower() == "exit":
                    print("Cerrando consola...")
                    self.running = False
                elif command.lower() == "swap":
                    nuevo_guild = seleccionar_servidor(self.connected_guilds)
                    if nuevo_guild is not None:
                        self.current_guild = nuevo_guild
                        print(f"Servidor actual: {getattr(self.current_guild, 'name', self.current_guild)} (ID: {getattr(self.current_guild, 'id', self.current_guild)})")
                        self.change_guild(self.current_guild)
                elif command:
                    self.handle_command(command)
            except (EOFError, KeyboardInterrupt):
                print("\nCerrando consola...")
                self.running = False

    def change_guild(self, guild_id):
        if guild_id in self.connected_guilds:
            self.current_guild = guild_id
            print(f"Cambiado al servidor: {self.current_guild}")
            self.build_guild_object(self.current_guild)
        else:
            print("Servidor no conectado.")

    def handle_command(self, command):
        # Comandos personalizados
        if command == "guilds":
            print(f"Servidores conectados: {self.bot.get_guild()}")
        elif command == "status":
            print(f"Bot conectado: {self.bot.is_ready()}")
        elif command == "setup db":
            setup_db(self.current_guild)
        elif command.startswith("setup referee"):
            parts = command.split()
            if len(parts) == 3 and parts[2] in ["eng", "esp"]:
                lang = parts[2]
                self.guild_language[getattr(self.current_guild, 'id', self.current_guild)] = lang
                self.build_guild_object(self.current_guild, lang)
                print(f"Referee configurado para el servidor con idioma: {lang}")
            else:
                print("Uso: setup referee [eng|esp]")
        elif command == "show lang":
            gid = getattr(self.current_guild, 'id', self.current_guild)
            lang = self.guild_language.get(gid, "eng")
            print(f"Idioma actual de la guild: {lang}")
        else:
            print(f"Comando desconocido: {command}")

    def build_guild_object(self, guild, lang_code=None):
        object_guild = GuildObject(bot=self.bot)
        # Construye el objeto GuildObject y asigna el idioma
        if lang_code is None:
            gid = getattr(guild, 'id', guild)
            lang_code = self.guild_language.get(gid, "eng")
        object_guild.set_id(guild.id if hasattr(guild, 'id') else guild)
        object_guild.set_name(guild.name if hasattr(guild, 'name') else guild)
        object_guild.set_version("1.0")
        object_guild.set_channels(guild.channels if hasattr(guild, 'channels') else [])
        object_guild.set_members(guild.members if hasattr(guild, 'members') else [])
        object_guild.set_roles(guild.roles if hasattr(guild, 'roles') else [])
        object_guild.set_categories(guild.categories if hasattr(guild, 'categories') else [])
        # Asigna el idioma usando LanguageManager
        import os
        locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'languages', 'locales')
        object_guild.lang_manager.lang_dir = locales_dir
        object_guild.lang_manager.lang_code = lang_code
        print(f"Construido objeto Guild: {object_guild} con idioma {lang_code}")
        self.bot.set_guild_object(object_guild)
        return

def start_console(bot):
    console = ConsoleManager(bot)
    console.start()
    return console
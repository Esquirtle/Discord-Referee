
import threading
from .console_utils import mostrar_servidores, seleccionar_servidor
from .setup_commands import setup_db
class ConsoleManager(threading.Thread):
    def __init__(self, bot, connected_guilds):
        super().__init__(daemon=True)
        self.bot = bot
        self.running = True
        self.connected_guilds = connected_guilds
        self.current_guild = None

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
            self.build_guild()
        else:
            print("Servidor no conectado.")

    def handle_command(self, command):
        # Aquí puedes agregar tus comandos personalizados
        if command == "guilds":
            print(f"Servidores conectados: {self.bot.get_guild()}")
        elif command == "status":
            print(f"Bot conectado: {self.bot.is_ready()}")
        elif command == "setup db":
            setup_db(self.current_guild)
        else:
            print(f"Comando desconocido: {command}")

    def build_guild(self):
        # Aquí puedes construir el objeto GuildObject con la información del servidor actual
        self.bot.guild_object.set_id(self.current_guild.id if hasattr(self.current_guild, 'id') else self.current_guild)
        self.bot.guild_object.set_name(self.current_guild.name if hasattr(self.current_guild, 'name') else self.current_guild)
        self.bot.guild_object.set_version("1.0")  # Puedes ajustar la versión según sea necesario
        #self.bot.guild_object.set_config(self.bot.config)  # Asignar la configuración del bot
        self.bot.guild_object.set_channels(self.current_guild.channels if hasattr(self.current_guild, 'channels') else [])
        self.bot.guild_object.set_members(self.current_guild.members if hasattr(self.current_guild, 'members') else [])
        self.bot.guild_object.set_roles(self.current_guild.roles if hasattr(self.current_guild, 'roles') else [])
        self.bot.guild_object.set_categories(self.current_guild.categories if hasattr(self.current_guild, 'categories') else [])
        print(f"Construido objeto Guild: {self.bot.guild_object}")
def start_console(bot):
    console = ConsoleManager(bot)
    console.start()
    return console
from .mgdb_manager import multi_db

class DatabaseManager:
    """
    Wrapper para usar el sistema multiguild (MultiGuildDatabase) con interfaz simplificada.
    """
    def __init__(self):
        self.db = multi_db

    def execute_query(self, guild_id, query, params=()):
        return self.db.execute_query(guild_id, query, params)

    def fetch_all(self, guild_id, query, params=()):
        return self.db.fetch_all(guild_id, query, params)

    def fetch_one(self, guild_id, query, params=()):
        return self.db.fetch_one(guild_id, query, params)

    def initialize_tables(self, guild_id):
        # Crea la base de datos y las tablas usando el sistema multiguild y los modelos centralizados
        return self.db.create_guild_database(guild_id, force=False)

    def close(self, guild_id=None):
        if guild_id is not None:
            self.db.disconnect_guild(guild_id)
        else:
            self.db.disconnect_all()

    def register_user(self, guild_id, discord_id, steam_id, user_type="player"):
        """
        Registra un usuario en la tabla users.
        """
        query = """
        INSERT INTO users (discord_id, steam_id, user_type)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE steam_id=VALUES(steam_id), user_type=VALUES(user_type)
        """
        return self.execute_query(guild_id, query, (discord_id, steam_id, user_type))

    def get_user_by_discord_id(self, guild_id, discord_id):
        """
        Busca un usuario por su discord_id.
        """
        query = "SELECT * FROM users WHERE discord_id = %s"
        return self.fetch_one(guild_id, query, (discord_id,))

    def get_user_by_steam_id(self, guild_id, steam_id):
        """
        Busca un usuario por su steam_id.
        """
        query = "SELECT * FROM users WHERE steam_id = %s"
        return self.fetch_one(guild_id, query, (steam_id,))
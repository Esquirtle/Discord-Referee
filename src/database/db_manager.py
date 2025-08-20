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
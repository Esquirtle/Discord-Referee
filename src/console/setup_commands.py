from database.db_manager import DatabaseManager

def setup_db(current_guild):
    """
    Crea la base de datos y las tablas para la guild actual usando el gestor multiguild.
    """
    if not current_guild:
        print("❌ No hay guild seleccionada.")
        return

    guild_id = getattr(current_guild, 'id', current_guild)
    db_manager = DatabaseManager()
    print(f"🔧 Iniciando setup de base de datos para guild {guild_id}...")
    success = db_manager.initialize_tables(guild_id)
    if success:
        print(f"✅ Base de datos y tablas creadas/verificadas para guild {guild_id}")
    else:
        print(f"❌ Error creando/verificando la base de datos para guild {guild_id}")
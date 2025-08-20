"""
Sistema de base de datos multi-guild unificado.
Combina DatabaseConnection y GuildDatabaseManager en una sola clase simplificada.
"""

import mysql.connector
from mysql.connector import Error
from typing import Dict, Any, Optional
import logging
from contextlib import contextmanager
from .mgdb_schema import DatabaseSchemaManager

class MultiGuildDatabase:
    """
    Sistema unificado de base de datos multi-guild.
    Gestiona conexiones independientes para cada servidor Discord.
    """
    def __init__(self, host: str = 'localhost', user: str = 'root', password: str = '', port: int = 3306):

        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connections: Dict[int, mysql.connector.MySQLConnection] = {}
        self.logger = logging.getLogger(__name__)
        self.schema_manager = DatabaseSchemaManager()
    
    def get_database_name(self, guild_id: int) -> str:

        return f"referee_guild_{guild_id}"
    
    def get_connection(self, guild_id: int, create_if_not_exists: bool = False) -> Optional[mysql.connector.MySQLConnection]:
        """
        Obtiene la conexión a la base de datos para un guild específico.
        
        Args:
            guild_id: ID del guild de Discord
            create_if_not_exists: Si True, crea la base de datos si no existe
            
        Returns:
            Conexión a MySQL o None si no existe y create_if_not_exists es False
        """
        if guild_id not in self.connections or not self.connections[guild_id].is_connected():
            database_name = self.get_database_name(guild_id)
            
            # Solo crear base de datos si se solicita explícitamente
            if create_if_not_exists:
                if not self._ensure_database_exists(database_name):
                    return None
            else:
                # Verificar si la base de datos existe
                if not self._database_exists(database_name):
                    return None
            
            # Crear conexión
            config = {
                'host': self.host,
                'database': database_name,
                'user': self.user,
                'password': self.password,
                'port': self.port,
                'autocommit': True,
                'charset': 'utf8mb4'
            }
            
            try:
                self.connections[guild_id] = mysql.connector.connect(**config)
                
                # Solo crear tablas si se solicita explícitamente
                if create_if_not_exists:
                    self._ensure_tables_exist(guild_id)
                    
            except Error as e:
                self.logger.error(f"Error conectando a base de datos para guild {guild_id}: {e}")
                return None
            
        return self.connections[guild_id]
    
    def _database_exists(self, database_name: str) -> bool:
        """Verifica si una base de datos existe."""
        try:
            temp_config = {
                'host': self.host,
                'user': self.user,
                'password': self.password,
                'port': self.port,
                'autocommit': True
            }
            
            temp_connection = mysql.connector.connect(**temp_config)
            cursor = temp_connection.cursor()
            
            cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{database_name}'")
            result = cursor.fetchone()
            
            cursor.close()
            temp_connection.close()
            
            return result is not None
            
        except Error as e:
            self.logger.error(f"Error verificando existencia de base de datos {database_name}: {e}")
            return False
    
    def create_guild_database(self, guild_id: int, force: bool = False) -> bool:
        """
        Crea la base de datos para un guild específico.
        
        Args:
            guild_id: ID del guild de Discord
            force: Si True, elimina la base de datos existente antes de crear una nueva
            
        Returns:
            bool: True si la operación fue exitosa
        """
        database_name = self.get_database_name(guild_id)
        
        try:
            temp_config = {
                'host': self.host,
                'user': self.user,
                'password': self.password,
                'port': self.port,
                'autocommit': True
            }
            
            temp_connection = mysql.connector.connect(**temp_config)
            cursor = temp_connection.cursor()
            
            # Si force=True, eliminar base de datos existente
            if force:
                cursor.execute(f"DROP DATABASE IF EXISTS `{database_name}`")
                print(f"🗑️ Base de datos existente eliminada: {database_name}")
            
            # Crear la nueva base de datos
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Base de datos creada: {database_name}")
            
            cursor.close()
            temp_connection.close()
            
            # Cerrar conexión existente si la hay
            if guild_id in self.connections:
                self.connections[guild_id].close()
                del self.connections[guild_id]
            
            # Crear las tablas
            connection = self.get_connection(guild_id, create_if_not_exists=True)
            if connection:
                print(f"✅ Estructura de tablas configurada para guild {guild_id}")
                return True
            else:
                print(f"❌ Error configurando estructura de tablas para guild {guild_id}")
                return False
                
        except Error as e:
            self.logger.error(f"Error creando base de datos para guild {guild_id}: {e}")
            print(f"❌ Error: {e}")
            return False
    
    def _ensure_database_exists(self, database_name: str) -> bool:
        """Crea la base de datos si no existe."""
        try:
            temp_config = {
                'host': self.host,
                'user': self.user,
                'password': self.password,
                'port': self.port,
                'autocommit': True
            }
            
            temp_connection = mysql.connector.connect(**temp_config)
            cursor = temp_connection.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            cursor.close()
            temp_connection.close()
            return True
            
        except Error as e:
            self.logger.error(f"Error creando base de datos {database_name}: {e}")
            return False
    
    def _ensure_tables_exist(self, guild_id: int) -> bool:
        """Crea las tablas necesarias si no existen usando el schema manager centralizado."""
        try:
            self.logger.info(f"Verificando/creando estructura de base de datos para guild {guild_id}")
            
            # Use centralized schema manager for consistent schema creation
            success_count, error_count = self.schema_manager.create_complete_schema_sync(guild_id, self)
            
            self.logger.info(f"Tablas verificadas/creadas para guild {guild_id}")
            return error_count == 0
            
        except Exception as e:
            self.logger.error(f"Error configurando tablas para guild {guild_id}: {e}")
            return False
    
    @contextmanager
    def get_cursor(self, guild_id: int):
        """
        Obtiene un cursor para la base de datos del guild.
        Si la base de datos no existe, lanza una excepción informativa.
        """
        connection = self.get_connection(guild_id, create_if_not_exists=False)
        if connection is None:
            database_name = self.get_database_name(guild_id)
            raise Error(f"Base de datos no encontrada: {database_name}. Ejecuta 'setup db' para crearla.")
        
        cursor = connection.cursor(dictionary=True)
        try:
            yield cursor
        except Error as e:
            self.logger.error(f"Error en la base de datos del guild {guild_id}: {e}")
            connection.rollback()
            raise
        finally:
            cursor.close()
    
    def fetch_one(self, guild_id: int, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        try:
            with self.get_cursor(guild_id) as cursor:
                if params:
                    # Debug logging
                    print(f"🔧 Executing query: {query}")
                    print(f"🔧 With params: {params}")
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchone()
                print(f"🔧 Query result: {result}")
                return result
        except Error as e:
            self.logger.error(f"Error en fetch_one para guild {guild_id}: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Params: {params}")
            print(f"❌ Database fetch error: {e}")
            return None
    
    def execute_query(self, guild_id: int, query: str, params: tuple = None) -> bool:
        """
        Ejecuta una consulta SQL en la base de datos del guild.
        """
        try:
            with self.get_cursor(guild_id) as cursor:
                if params:
                    # Debug logging
                    print(f"🔧 Executing query: {query}")
                    print(f"🔧 With params: {params}")
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.logger.info(f"Query ejecutada exitosamente en guild {guild_id}")
                print(f"✅ Query executed successfully")
                return True
        except Error as e:
            self.logger.error(f"Error ejecutando consulta en guild {guild_id}: {e}")
            self.logger.error(f"Query: {query}")
            self.logger.error(f"Params: {params}")
            print(f"❌ Database error: {e}")
            return False
    
    def fetch_all(self, guild_id: int, query: str, params: tuple = None) -> list:
        try:
            with self.get_cursor(guild_id) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
        except Error as e:
            self.logger.error(f"Error en fetch_all para guild {guild_id}: {e}")
            self.logger.error(f"Query: {query}")  
            self.logger.error(f"Params: {params}")
            print(f"❌ Database fetch_all error: {e}")
            return []

    def get_last_insert_id(self, guild_id: int) -> Optional[int]:
        try:
            with self.get_cursor(guild_id) as cursor:
                cursor.execute("SELECT LAST_INSERT_ID()")
                result = cursor.fetchone()
                return result['LAST_INSERT_ID()'] if result else None
        except Error as e:
            self.logger.error(f"Error obteniendo last insert id para guild {guild_id}: {e}")
            return None
    
    def disconnect_guild(self, guild_id: int):
        """Desconecta una conexión específica de guild."""
        if guild_id in self.connections:
            if self.connections[guild_id].is_connected():
                self.connections[guild_id].close()
            del self.connections[guild_id]
    
    def disconnect_all(self):
        """Desconecta todas las conexiones activas."""
        for guild_id in list(self.connections.keys()):
            self.disconnect_guild(guild_id)
    
    def migrate_guild_database(self, guild_id: int) -> bool:
        """
        Migra la base de datos de un guild a la última versión del esquema.
        
        Args:
            guild_id: ID del guild de Discord
            
        Returns:
            bool: True si la migración fue exitosa
        """
        try:
            print(f"🔄 Iniciando migración de base de datos para guild {guild_id}...")
            
            # Verificar que la base de datos existe
            connection = self.get_connection(guild_id, create_if_not_exists=False)
            if connection is None:
                print(f"❌ No se encontró base de datos para guild {guild_id}")
                return False
            
            # Ejecutar migraciones
            success_count, error_count = self.schema_manager.migrate_database_schema(guild_id, self)
            
            if error_count == 0:
                print(f"✅ Migración completada exitosamente para guild {guild_id}")
                return True
            else:
                print(f"⚠️ Migración completada con {error_count} errores para guild {guild_id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error migrando base de datos para guild {guild_id}: {e}")
            print(f"❌ Error durante la migración: {e}")
            return False
    
    def close_all_connections(self):
        """Cierra todas las conexiones de base de datos."""
        try:
            closed_count = 0
            
            # Close connections in the pool
            for guild_id, connection in list(self.connections.items()):
                try:
                    if connection and connection.is_connected():
                        connection.close()
                        closed_count += 1
                    del self.connections[guild_id]
                except Exception as e:
                    print(f"⚠️ Error cerrando conexión para guild {guild_id}: {e}")
            
            # Clear the pool
            self.connections.clear()
            
            print(f"✅ {closed_count} conexiones de base de datos cerradas")
            return True
            
        except Exception as e:
            print(f"❌ Error cerrando conexiones de base de datos: {e}")
            return False

    def __del__(self):
        """Destructor para limpiar conexiones."""
        self.close_all_connections()

multi_db = MultiGuildDatabase()
"""
Centralized database schema management for dcGoal.
Handles all database creation, migration, and schema operations.
"""

import os
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional
import logging

class DatabaseSchemaManager:
    """
    Centralized database schema management.
    Ensures all database operations use the same schema definitions.
    """
    
    def __init__(self, host: str = 'localhost', user: str = 'root', password: str = '', port: int = 3306):
        """Initialize the schema manager with database connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.logger = logging.getLogger(__name__)
    
    def get_database_name(self, guild_id: int) -> str:
        """Generate the standardized database name for a guild."""
        return f"goalier_guild_{guild_id}"
    
    def get_table_definitions(self) -> List[str]:
        """
        Get standardized table definitions matching create_database.sql.
        All database creation should use these definitions.
        """
        return [
            # Users table - base for all users
            """
            CREATE TABLE IF NOT EXISTS users (
                discord_id BIGINT PRIMARY KEY,
                steam_id VARCHAR(50) NOT NULL UNIQUE,
                user_type ENUM('player', 'admin') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Players table - extends users for players
            """
            CREATE TABLE IF NOT EXISTS players (
                discord_id BIGINT PRIMARY KEY,
                display_name VARCHAR(100) NULL,
                ranking INT DEFAULT 0,
                win INT DEFAULT 0,
                loss INT DEFAULT 0,
                FOREIGN KEY (discord_id) REFERENCES users(discord_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Admins table - extends users for admins
            """
            CREATE TABLE IF NOT EXISTS admins (
                discord_id BIGINT PRIMARY KEY,
                int_privileges INT DEFAULT 1,
                FOREIGN KEY (discord_id) REFERENCES users(discord_id) ON DELETE CASCADE,
                CHECK (int_privileges IN (1, 2, 3))
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Scrims table - main matches/scrims
            """
            CREATE TABLE IF NOT EXISTS scrims (
                scrim_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                match_code VARCHAR(20) NOT NULL UNIQUE,
                dc_channel_id BIGINT NOT NULL,
                division VARCHAR(50) NOT NULL,
                creator_discord_id BIGINT NOT NULL,
                description VARCHAR(255),
                local_score INT DEFAULT 0,
                away_score INT DEFAULT 0,
                status ENUM('pending', 'in_progress', 'finished', 'cancelled') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_discord_id) REFERENCES players(discord_id),
                CHECK (local_score >= 0),
                CHECK (away_score >= 0)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Teams table - teams within scrims
            """
            CREATE TABLE IF NOT EXISTS teams (
                team_id INT AUTO_INCREMENT PRIMARY KEY,
                scrim_id VARCHAR(50) NOT NULL,
                team_type ENUM('local', 'away') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scrim_id) REFERENCES scrims(scrim_id) ON DELETE CASCADE,
                UNIQUE KEY unique_team_per_scrim (scrim_id, team_type)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Team players relation table
            """
            CREATE TABLE IF NOT EXISTS team_players (
                team_id INT,
                player_discord_id BIGINT,
                player_steam_id VARCHAR(50) NOT NULL,
                scrim_id VARCHAR(50) NOT NULL,
                team_type ENUM('local', 'away') NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (team_id, player_discord_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
                FOREIGN KEY (player_discord_id) REFERENCES players(discord_id) ON DELETE CASCADE,
                FOREIGN KEY (scrim_id) REFERENCES scrims(scrim_id) ON DELETE CASCADE,
                FOREIGN KEY (player_steam_id) REFERENCES users(steam_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Match history table
            """
            CREATE TABLE IF NOT EXISTS match_history (
                history_id INT AUTO_INCREMENT PRIMARY KEY,
                scrim_id VARCHAR(50) NOT NULL,
                player_discord_id BIGINT NOT NULL,
                team_type ENUM('local', 'away') NOT NULL,
                result ENUM('win', 'loss', 'tie') NOT NULL,
                final_local_score INT NOT NULL,
                final_away_score INT NOT NULL,
                match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scrim_id) REFERENCES scrims(scrim_id),
                FOREIGN KEY (player_discord_id) REFERENCES players(discord_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Guild configuration table
            """
            CREATE TABLE IF NOT EXISTS guild_config (
                guild_id BIGINT PRIMARY KEY,
                guild_name VARCHAR(255),
                setup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                admin_role_id BIGINT,
                player_role_id BIGINT,
                scrims_category_id BIGINT,
                active BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tournaments table - main tournaments
            """
            CREATE TABLE IF NOT EXISTS tournaments (
                tournament_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                format_type ENUM('single_elimination', 'double_elimination', 'round_robin', 'swiss') DEFAULT 'single_elimination',
                max_teams INT DEFAULT 16,
                creator_discord_id BIGINT NOT NULL,
                status ENUM('draft', 'registration_open', 'registration_closed', 'in_progress', 'completed', 'cancelled') DEFAULT 'draft',
                start_date TIMESTAMP NULL,
                end_date TIMESTAMP NULL,
                winner_team_id VARCHAR(50) NULL,
                prize_pool TEXT NULL,
                rules TEXT NULL,
                category_id BIGINT NULL,
                info_channel_id BIGINT NULL,
                bracket_channel_id BIGINT NULL,
                admin_channel_id BIGINT NULL,
                announcements_channel_id BIGINT NULL,
                matching_strategy ENUM('random', 'seeded') DEFAULT 'random',
                current_round INT DEFAULT 1,
                teams_remaining INT DEFAULT 0,
                started_at TIMESTAMP NULL,
                completed_at TIMESTAMP NULL,
                notes TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_discord_id) REFERENCES players(discord_id),
                CHECK (max_teams >= 2 AND max_teams <= 128),
                CHECK (current_round >= 1),
                CHECK (teams_remaining >= 0)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tournament teams table - teams participating in tournaments
            """
            CREATE TABLE IF NOT EXISTS tournament_teams (
                team_id VARCHAR(50) PRIMARY KEY,
                tournament_id VARCHAR(50) NOT NULL,
                name VARCHAR(100) NOT NULL,
                captain_discord_id BIGINT NOT NULL,
                channel_id BIGINT NULL,
                active BOOLEAN DEFAULT TRUE,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
                FOREIGN KEY (captain_discord_id) REFERENCES players(discord_id),
                UNIQUE KEY unique_team_name_per_tournament (tournament_id, name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Captains table - manages team captains and their privileges
            """
            CREATE TABLE IF NOT EXISTS captains (
                captain_id INT AUTO_INCREMENT PRIMARY KEY,
                discord_id BIGINT NOT NULL,
                team_id VARCHAR(50) NOT NULL,
                tournament_id VARCHAR(50) NOT NULL,
                appointed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                appointed_by BIGINT NULL,
                active BOOLEAN DEFAULT TRUE,
                privileges TEXT NULL,
                FOREIGN KEY (discord_id) REFERENCES players(discord_id) ON DELETE CASCADE,
                FOREIGN KEY (team_id) REFERENCES tournament_teams(team_id) ON DELETE CASCADE,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
                FOREIGN KEY (appointed_by) REFERENCES players(discord_id) ON DELETE SET NULL,
                UNIQUE KEY unique_captain_per_team (team_id, tournament_id),
                INDEX idx_captain_discord (discord_id),
                INDEX idx_captain_team (team_id),
                INDEX idx_captain_tournament (tournament_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tournament players table - players in tournament teams (simplified)
            """
            CREATE TABLE IF NOT EXISTS tournament_players (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tournament_id VARCHAR(50) NOT NULL,
                team_id VARCHAR(50) NOT NULL,
                discord_id BIGINT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
                FOREIGN KEY (team_id) REFERENCES tournament_teams(team_id) ON DELETE CASCADE,
                FOREIGN KEY (discord_id) REFERENCES players(discord_id) ON DELETE CASCADE,
                UNIQUE KEY unique_player_per_tournament (tournament_id, discord_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Team invitations table - manages team invitations
            """
            CREATE TABLE IF NOT EXISTS team_invitations (
                invitation_id VARCHAR(50) PRIMARY KEY,
                team_id VARCHAR(50) NOT NULL,
                invited_discord_id BIGINT NOT NULL,
                inviter_discord_id BIGINT NOT NULL,
                status ENUM('pending', 'accepted', 'declined', 'expired') DEFAULT 'pending',
                message TEXT NULL,
                expires_at TIMESTAMP NULL,
                responded_at TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES tournament_teams(team_id) ON DELETE CASCADE,
                FOREIGN KEY (invited_discord_id) REFERENCES players(discord_id) ON DELETE CASCADE,
                FOREIGN KEY (inviter_discord_id) REFERENCES players(discord_id) ON DELETE CASCADE,
                UNIQUE KEY unique_team_invitation (team_id, invited_discord_id),
                INDEX idx_invited_user (invited_discord_id),
                INDEX idx_inviter_user (inviter_discord_id),
                INDEX idx_status (status),
                INDEX idx_expires (expires_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tournament brackets table - simplified bracket organization
            """
            CREATE TABLE IF NOT EXISTS tournament_brackets (
                bracket_id VARCHAR(50) PRIMARY KEY,
                tournament_id VARCHAR(50) NOT NULL,
                phase VARCHAR(50) NOT NULL,
                round_number INT NOT NULL,
                winner_team_id VARCHAR(50) NULL,
                runner_up_team_id VARCHAR(50) NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
                FOREIGN KEY (winner_team_id) REFERENCES tournament_teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (runner_up_team_id) REFERENCES tournament_teams(team_id) ON DELETE SET NULL,
                INDEX idx_tournament_round (tournament_id, round_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tournament matches table - using game_id reference
            """
            CREATE TABLE IF NOT EXISTS tournament_matches (
                match_id VARCHAR(50) PRIMARY KEY,
                tournament_id VARCHAR(50) NOT NULL,
                bracket_id VARCHAR(50) NOT NULL,
                game_id INT NULL,
                team1_id VARCHAR(50) NULL,
                team2_id VARCHAR(50) NULL,
                match_number INT NOT NULL,
                round_number INT NOT NULL,
                winner_team_id VARCHAR(50) NULL,
                team1_score INT NULL DEFAULT 0,
                team2_score INT NULL DEFAULT 0,
                completed_at TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
                FOREIGN KEY (bracket_id) REFERENCES tournament_brackets(bracket_id) ON DELETE CASCADE,
                FOREIGN KEY (team1_id) REFERENCES tournament_teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (team2_id) REFERENCES tournament_teams(team_id) ON DELETE SET NULL,
                FOREIGN KEY (winner_team_id) REFERENCES tournament_teams(team_id) ON DELETE SET NULL,
                CHECK (team1_score >= 0),
                CHECK (team2_score >= 0),
                INDEX idx_tournament_round_match (tournament_id, round_number, match_number)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Tournament statistics table for tracking tournament completion data
            """
            CREATE TABLE IF NOT EXISTS tournament_statistics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tournament_id VARCHAR(50) NOT NULL,
                total_teams INT DEFAULT 0,
                total_matches INT DEFAULT 0,
                total_rounds INT DEFAULT 0,
                winner_team_id VARCHAR(50) NULL,
                end_reason TEXT NULL,
                duration_minutes INT NULL,
                participants_count INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE CASCADE,
                FOREIGN KEY (winner_team_id) REFERENCES tournament_teams(team_id) ON DELETE SET NULL,
                UNIQUE KEY unique_tournament_stats (tournament_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Registrations table for player registration tracking
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_id BIGINT NOT NULL,
                team_id INT NULL,
                status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(discord_id) ON DELETE CASCADE,
                FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        ]
    
    def get_index_definitions(self) -> List[str]:
        """Get standardized index definitions for optimization."""
        return [
            "CREATE INDEX IF NOT EXISTS idx_users_steam_id ON users(steam_id)",
            "CREATE INDEX IF NOT EXISTS idx_players_display_name ON players(display_name)",
            "CREATE INDEX IF NOT EXISTS idx_scrims_creator ON scrims(creator_discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_scrims_status ON scrims(status)",
            "CREATE INDEX IF NOT EXISTS idx_scrims_division ON scrims(division)",
            "CREATE INDEX IF NOT EXISTS idx_match_history_player ON match_history(player_discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_match_history_date ON match_history(match_date)",
            "CREATE INDEX IF NOT EXISTS idx_team_players_player ON team_players(player_discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournaments_creator ON tournaments(creator_discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournaments_status ON tournaments(status)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_teams_captain ON tournament_teams(captain_discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_teams_tournament ON tournament_teams(tournament_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_teams_channel ON tournament_teams(channel_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_players_team ON tournament_players(team_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_players_discord ON tournament_players(discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_team_invitations_invited ON team_invitations(invited_discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_team_invitations_status ON team_invitations(status)",
            "CREATE INDEX IF NOT EXISTS idx_team_invitations_team ON team_invitations(team_id)",
            "CREATE INDEX IF NOT EXISTS idx_captains_discord ON captains(discord_id)",
            "CREATE INDEX IF NOT EXISTS idx_captains_team ON captains(team_id)",
            "CREATE INDEX IF NOT EXISTS idx_captains_tournament ON captains(tournament_id)",
            "CREATE INDEX IF NOT EXISTS idx_captains_active ON captains(active)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_statistics_tournament ON tournament_statistics(tournament_id)",
            "CREATE INDEX IF NOT EXISTS idx_tournament_statistics_winner ON tournament_statistics(winner_team_id)"
        ]
    
    def get_view_definitions(self) -> List[str]:
        """Get standardized view definitions for complex queries."""
        return [
            # Player stats view
            """
            CREATE OR REPLACE VIEW player_stats AS
            SELECT 
                p.discord_id,
                u.steam_id,
                p.ranking,
                p.win,
                p.loss,
                (p.win + p.loss) AS total_games,
                CASE 
                    WHEN (p.win + p.loss) = 0 THEN 0.0
                    ELSE ROUND((p.win / (p.win + p.loss)) * 100, 2)
                END AS win_rate,
                u.created_at AS registered_at
            FROM players p
            JOIN users u ON p.discord_id = u.discord_id
            """,
            
            # Scrim details view
            """
            CREATE OR REPLACE VIEW scrim_details AS
            SELECT 
                s.scrim_id,
                s.name,
                s.match_code,
                s.dc_channel_id,
                s.division,
                s.creator_discord_id,
                u.steam_id AS creator_steam_id,
                s.local_score,
                s.away_score,
                s.status,
                s.created_at,
                s.updated_at,
                CASE 
                    WHEN s.local_score > s.away_score THEN 'local'
                    WHEN s.away_score > s.local_score THEN 'away'
                    ELSE 'tie'
                END AS winner
            FROM scrims s
            JOIN users u ON s.creator_discord_id = u.discord_id
            """,
            
            # Team info view
            """
            CREATE OR REPLACE VIEW team_info AS
            SELECT 
                t.team_id,
                t.scrim_id,
                t.team_type,
                COUNT(tp.player_discord_id) AS player_count,
                GROUP_CONCAT(tp.player_discord_id) AS player_discord_ids,
                GROUP_CONCAT(tp.player_steam_id) AS player_steam_ids,
                GROUP_CONCAT(CONCAT(tp.player_steam_id, '(', tp.player_discord_id, ')') SEPARATOR ', ') AS players_info
            FROM teams t
            LEFT JOIN team_players tp ON t.team_id = tp.team_id
            GROUP BY t.team_id, t.scrim_id, t.team_type
            """,
            
            # Scrim teams view
            """
            CREATE OR REPLACE VIEW scrim_teams AS
            SELECT 
                s.scrim_id,
                s.name AS scrim_name,
                s.match_code,
                s.division,
                s.local_score,
                s.away_score,
                s.status,
                local_team.player_count AS local_players_count,
                local_team.player_steam_ids AS local_steam_ids,
                away_team.player_count AS away_players_count,
                away_team.player_steam_ids AS away_steam_ids
            FROM scrims s
            LEFT JOIN team_info local_team ON s.scrim_id = local_team.scrim_id AND local_team.team_type = 'local'
            LEFT JOIN team_info away_team ON s.scrim_id = away_team.scrim_id AND away_team.team_type = 'away'
            """,
            
            # Team invitations view
            """
            CREATE OR REPLACE VIEW team_invitations_view AS
            SELECT 
                ti.invitation_id,
                ti.team_id,
                ti.invited_discord_id,
                ti.inviter_discord_id,
                ti.status,
                ti.message,
                ti.expires_at,
                ti.responded_at,
                ti.created_at,
                ti.updated_at,
                tt.name AS team_name,
                tt.tournament_id,
                t.name AS tournament_name,
                invited_player.display_name AS invited_player_name,
                inviter_player.display_name AS inviter_player_name,
                CASE 
                    WHEN ti.expires_at < NOW() AND ti.status = 'pending' THEN 'expired'
                    ELSE ti.status
                END AS current_status
            FROM team_invitations ti
            JOIN tournament_teams tt ON ti.team_id = tt.team_id
            JOIN tournaments t ON tt.tournament_id = t.tournament_id
            LEFT JOIN players invited_player ON ti.invited_discord_id = invited_player.discord_id
            LEFT JOIN players inviter_player ON ti.inviter_discord_id = inviter_player.discord_id
            """,
            
            # Tournament team details view
            """
            CREATE OR REPLACE VIEW tournament_team_details AS
            SELECT 
                tt.team_id,
                tt.tournament_id,
                tt.name AS team_name,
                tt.captain_discord_id,
                tt.active,
                tt.registration_date,
                t.name AS tournament_name,
                t.status AS tournament_status,
                t.format_type,
                captain.display_name AS captain_name,
                COUNT(tp.discord_id) AS player_count,
                GROUP_CONCAT(tp.discord_id) AS player_discord_ids
            FROM tournament_teams tt
            JOIN tournaments t ON tt.tournament_id = t.tournament_id
            LEFT JOIN players captain ON tt.captain_discord_id = captain.discord_id
            LEFT JOIN tournament_players tp ON tt.team_id = tp.team_id
            GROUP BY tt.team_id, tt.tournament_id, tt.name, tt.captain_discord_id, 
                     tt.active, tt.registration_date, t.name, t.status, t.format_type, captain.display_name
            """,
            
            # Captain details view
            """
            CREATE OR REPLACE VIEW captain_details AS
            SELECT 
                c.captain_id,
                c.discord_id,
                c.team_id,
                c.tournament_id,
                c.appointed_at,
                c.appointed_by,
                c.active,
                c.privileges,
                p.discord_id AS captain_name,
                tt.name AS team_name,
                t.name AS tournament_name,
                appointer.display_name AS appointed_by_name,
                COUNT(tp.discord_id) AS team_player_count
            FROM captains c
            JOIN players p ON c.discord_id = p.discord_id
            JOIN tournament_teams tt ON c.team_id = tt.team_id
            JOIN tournaments t ON c.tournament_id = t.tournament_id
            LEFT JOIN players appointer ON c.appointed_by = appointer.discord_id
            LEFT JOIN tournament_players tp ON c.team_id = tp.team_id
            GROUP BY c.captain_id, c.discord_id, c.team_id, c.tournament_id, c.appointed_at,
                     c.appointed_by, c.active, c.privileges, p.discord_id, tt.name, t.name, appointer.display_name
            """
        ]
    
    async def create_database(self, guild_id: int) -> bool:
        """Create database for a guild if it doesn't exist."""
        db_name = self.get_database_name(guild_id)
        
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            cursor.close()
            connection.close()
            
            self.logger.info(f"Database {db_name} created or verified")
            return True
            
        except Error as e:
            self.logger.error(f"Error creating database {db_name}: {e}")
            return False
    
    async def create_complete_schema(self, guild_id: int, multi_db_instance) -> bool:
        """
        Create complete schema for a guild using the centralized definitions.
        
        Args:
            guild_id: Discord guild ID
            multi_db_instance: MultiGuildDatabase instance for query execution
        """
        try:
            # Ensure database exists
            await self.create_database(guild_id)
            
            # Create tables
            print("📋 Creando estructura de tablas...")
            tables = self.get_table_definitions()
            
            for i, table_sql in enumerate(tables, 1):
                try:
                    multi_db_instance.execute_query(guild_id, table_sql)
                    table_name = self._extract_table_name(table_sql)
                    print(f"   ✅ Tabla {i}/{len(tables)}: {table_name}")
                except Exception as e:
                    table_name = self._extract_table_name(table_sql)
                    print(f"   ❌ Error tabla {table_name}: {e}")
                    self.logger.error(f"Error creating table {table_name}: {e}")
            
            print("✅ Estructura de tablas completada")
            
            # Create indexes
            print("📋 Creando índices de optimización...")
            indexes = self.get_index_definitions()
            
            for i, index_sql in enumerate(indexes, 1):
                try:
                    multi_db_instance.execute_query(guild_id, index_sql)
                    print(f"   ✅ Índice {i}/{len(indexes)}: {index_sql.split()[-2]}")
                except Exception as e:
                    print(f"   ❌ Error índice {i}: {e}")
                    self.logger.error(f"Error creating index: {e}")
            
            print("✅ Índices creados exitosamente")
            
            # Create views
            print("📋 Creando vistas de consulta...")
            views = self.get_view_definitions()
            
            for i, view_sql in enumerate(views, 1):
                try:
                    multi_db_instance.execute_query(guild_id, view_sql)
                    view_name = self._extract_view_name(view_sql)
                    print(f"   ✅ Vista {i}/{len(views)}: {view_name}")
                except Exception as e:
                    view_name = self._extract_view_name(view_sql)
                    print(f"   ❌ Error vista {view_name}: {e}")
                    self.logger.error(f"Error creating view {view_name}: {e}")
            
            print("✅ Vistas creadas exitosamente")
            
            # Insert guild configuration
            print("📋 Insertando configuración inicial...")
            config_sql = """
            INSERT INTO guild_config (guild_id, setup_date) 
            VALUES (%s, NOW()) 
            ON DUPLICATE KEY UPDATE setup_date = NOW()
            """
            multi_db_instance.execute_query(guild_id, config_sql, (guild_id,))
            print(f"   ✅ Configuración del guild {guild_id} insertada")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating complete schema for guild {guild_id}: {e}")
            return False
    
    def _extract_table_name(self, sql: str) -> str:
        """Extract table name from CREATE TABLE statement."""
        try:
            return sql.split('CREATE TABLE IF NOT EXISTS ')[1].split(' ')[0].strip()
        except:
            return "unknown"
    
    def _extract_view_name(self, sql: str) -> str:
        """Extract view name from CREATE VIEW statement."""
        try:
            return sql.split('CREATE OR REPLACE VIEW ')[1].split(' ')[0].strip()
        except:
            return "unknown"
    
    async def verify_schema(self, guild_id: int, multi_db_instance) -> Dict[str, Any]:
        """
        Verify that all required tables and columns exist for a guild.
        
        Returns:
            dict: Verification results with details about each table
        """
        db_name = self.get_database_name(guild_id)
        
        # Define required schema structure
        required_tables = {
            'users': ['discord_id', 'steam_id', 'user_type', 'created_at', 'updated_at'],
            'players': ['discord_id', 'display_name', 'ranking', 'win', 'loss'],
            'admins': ['discord_id', 'int_privileges'],
            'scrims': ['scrim_id', 'name', 'match_code', 'dc_channel_id', 'division', 
                      'creator_discord_id', 'local_score', 'away_score', 'status', 
                      'created_at', 'updated_at'],
            'teams': ['team_id', 'scrim_id', 'team_type', 'created_at'],
            'team_players': ['team_id', 'player_discord_id', 'player_steam_id', 
                           'scrim_id', 'team_type', 'joined_at'],
            'match_history': ['history_id', 'scrim_id', 'player_discord_id', 
                            'team_type', 'result', 'final_local_score', 
                            'final_away_score', 'match_date'],
            'guild_config': ['guild_id', 'guild_name', 'setup_date', 'admin_role_id', 
                           'player_role_id', 'scrims_category_id', 'active'],
            'tournaments': ['tournament_id', 'name', 'description', 'format_type', 
                          'max_teams', 'creator_discord_id', 'status', 'start_date', 
                          'end_date', 'winner_team_id', 'prize_pool', 'rules',
                          'category_id', 'info_channel_id', 'bracket_channel_id',
                          'admin_channel_id', 'announcements_channel_id', 'matching_strategy',
                          'started_at', 'completed_at', 'notes', 'created_at', 'updated_at'],
            'tournament_teams': ['team_id', 'tournament_id', 'name', 'captain_discord_id', 
                               'channel_id', 'active', 'registration_date'],
            'tournament_players': ['id', 'tournament_id', 'team_id', 'discord_id', 'joined_at'],
            'captains': ['captain_id', 'discord_id', 'team_id', 'tournament_id', 
                        'appointed_at', 'appointed_by', 'active', 'privileges'],
            'team_invitations': ['invitation_id', 'team_id', 'invited_discord_id', 
                                'inviter_discord_id', 'status', 'message', 'expires_at', 
                                'responded_at', 'created_at', 'updated_at'],
            'tournament_brackets': ['bracket_id', 'tournament_id', 'phase', 'round_number', 
                                  'winner_team_id', 'runner_up_team_id', 'completed', 'created_at'],
            'tournament_matches': ['match_id', 'tournament_id', 'bracket_id', 'game_id', 
                                 'team1_id', 'team2_id', 'match_number', 'round_number', 
                                 'winner_team_id', 'team1_score', 'team2_score', 
                                 'completed_at', 'created_at'],
            'tournament_statistics': ['id', 'tournament_id', 'total_teams', 'total_matches', 
                                    'total_rounds', 'winner_team_id', 'end_reason', 
                                    'duration_minutes', 'participants_count', 'created_at'],
            'registrations': ['id', 'player_id', 'team_id', 'status', 'created_at']
        }
        
        verification_results = {
            'database_name': db_name,
            'tables': {},
            'all_good': True,
            'missing_tables': [],
            'tables_with_issues': []
        }
        
        for table_name, required_columns in required_tables.items():
            try:
                # Check if table exists
                result = multi_db_instance.fetch_one(
                    guild_id,
                    f"SHOW TABLES LIKE '{table_name}'"
                )
                
                if not result:
                    verification_results['tables'][table_name] = {
                        'exists': False,
                        'columns': [],
                        'missing_columns': required_columns
                    }
                    verification_results['missing_tables'].append(table_name)
                    verification_results['all_good'] = False
                    continue
                
                # Check columns
                columns_result = multi_db_instance.fetch_all(
                    guild_id,
                    f"SHOW COLUMNS FROM {table_name}"
                )
                
                existing_columns = [col['Field'] for col in columns_result] if columns_result else []
                missing_columns = [col for col in required_columns if col not in existing_columns]
                
                verification_results['tables'][table_name] = {
                    'exists': True,
                    'columns': existing_columns,
                    'missing_columns': missing_columns
                }
                
                if missing_columns:
                    verification_results['tables_with_issues'].append(table_name)
                    verification_results['all_good'] = False
                
            except Exception as e:
                verification_results['tables'][table_name] = {
                    'exists': False,
                    'error': str(e)
                }
                verification_results['all_good'] = False
                self.logger.error(f"Error verifying table {table_name}: {e}")
        
        return verification_results
    
    def print_verification_results(self, results: Dict[str, Any]):
        """Print formatted verification results."""
        print(f"\n📋 Verificación de esquema - {results['database_name']}")
        print("-" * 60)
        
        for table_name, table_info in results['tables'].items():
            if not table_info.get('exists', False):
                if 'error' in table_info:
                    print(f"  ❌ Tabla '{table_name}': ERROR - {table_info['error']}")
                else:
                    print(f"  ❌ Tabla '{table_name}': NO EXISTE")
            elif table_info.get('missing_columns'):
                missing = ', '.join(table_info['missing_columns'])
                print(f"  ⚠️ Tabla '{table_name}': Faltan columnas: {missing}")
            else:
                column_count = len(table_info.get('columns', []))
                print(f"  ✅ Tabla '{table_name}': OK ({column_count} columnas)")
        
        print("-" * 60)
        if results['all_good']:
            print("🎉 ¡Esquema de base de datos verificado correctamente!")
        else:
            print("⚠️ Se encontraron problemas en el esquema de base de datos")
            if results['missing_tables']:
                print(f"📋 Tablas faltantes: {', '.join(results['missing_tables'])}")
            if results['tables_with_issues']:
                print(f"⚠️ Tablas con problemas: {', '.join(results['tables_with_issues'])}")
    
    def create_complete_schema_sync(self, guild_id: int, db_connection) -> tuple[int, int]:
        """
        Synchronous version of create_complete_schema for use with MultiGuildDatabase.
        Creates the complete database schema including tables, indexes, and views.
        
        Args:
            guild_id (int): Guild ID for the database
            db_connection: Database connection object with execute_query method
            
        Returns:
            tuple[int, int]: (success_count, error_count)
        """
        success_count = 0
        error_count = 0
        
        try:
            # Create tables
            print("📋 Creando estructura de tablas...")
            tables = self.get_table_definitions()
            
            for i, table_sql in enumerate(tables, 1):
                try:
                    # Use the connection's execute_query method directly
                    db_connection.execute_query(guild_id, table_sql)
                    # Extract table name from SQL for logging
                    table_name = table_sql.split('CREATE TABLE IF NOT EXISTS ')[1].split(' ')[0]
                    print(f"   ✅ Tabla {i}/{len(tables)}: {table_name}")
                    success_count += 1
                except Exception as e:
                    print(f"   ❌ Error tabla {i}: {e}")
                    error_count += 1
            
            # Create indexes
            print("📋 Creando índices de optimización...")
            indexes = self.get_index_definitions()
            
            for i, index_sql in enumerate(indexes, 1):
                try:
                    db_connection.execute_query(guild_id, index_sql)
                    index_name = index_sql.split('CREATE INDEX IF NOT EXISTS ')[1].split(' ')[0]
                    print(f"   ✅ Índice {i}/{len(indexes)}: {index_name}")
                    success_count += 1
                except Exception as e:
                    if "Duplicate key name" not in str(e):
                        print(f"   ⚠️ Error índice {i}: {e}")
                        error_count += 1
                    else:
                        print(f"   ℹ️ Índice {i}: Ya existe")
                        success_count += 1
            
            # Create views
            print("📋 Creando vistas de consulta...")
            views = self.get_view_definitions()
            
            for i, view_sql in enumerate(views, 1):
                try:
                    db_connection.execute_query(guild_id, view_sql)
                    view_name = view_sql.split('CREATE OR REPLACE VIEW ')[1].split(' ')[0]
                    print(f"   ✅ Vista {i}/{len(views)}: {view_name}")
                    success_count += 1
                except Exception as e:
                    print(f"   ⚠️ Error vista {i}: {e}")
                    error_count += 1
            
            # Insert initial guild configuration
            print("📋 Insertando configuración inicial...")
            config_sql = """
            INSERT INTO guild_config (guild_id, setup_date, active) 
            VALUES (%s, NOW(), TRUE) 
            ON DUPLICATE KEY UPDATE setup_date = NOW(), active = TRUE
            """
            try:
                db_connection.execute_query(guild_id, config_sql, (guild_id,))
                print("   ✅ Configuración del guild insertada")
                success_count += 1
            except Exception as e:
                print(f"   ❌ Error insertando configuración: {e}")
                error_count += 1
            
            print(f"✅ Esquema de base de datos completado: {success_count} exitosos, {error_count} errores")
            
        except Exception as e:
            print(f"❌ Error creando esquema completo: {e}")
            error_count += 1
        
        return success_count, error_count
    
    def get_migration_queries(self) -> List[str]:
        """
        Get database migration queries to update existing schemas.
        These queries check for column existence before adding them.
        """
        return [
            # Check and add missing columns to tournaments table
            """
            SELECT COUNT(*) as col_exists FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tournaments' AND COLUMN_NAME = 'current_round'
            """,
            "ALTER TABLE tournaments ADD COLUMN current_round INT DEFAULT 1",
            
            """
            SELECT COUNT(*) as col_exists FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tournaments' AND COLUMN_NAME = 'teams_remaining'
            """,
            "ALTER TABLE tournaments ADD COLUMN teams_remaining INT DEFAULT 0",
            
            """
            SELECT COUNT(*) as col_exists FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tournaments' AND COLUMN_NAME = 'completed_at'
            """,
            "ALTER TABLE tournaments ADD COLUMN completed_at TIMESTAMP NULL",
            
            # Fix tournament_matches table game_id column type
            "ALTER TABLE tournament_matches MODIFY COLUMN game_id BIGINT NULL"
        ]
    
    def migrate_database_schema(self, guild_id: int, db_connection) -> tuple[int, int]:
        """
        Migrates an existing database schema to the latest version.
        
        Args:
            guild_id (int): Guild ID for the database
            db_connection: Database connection object with execute_query method
            
        Returns:
            tuple[int, int]: (success_count, error_count)
        """
        success_count = 0
        error_count = 0
        
        try:
            print(f"🔄 Migrando esquema de base de datos para guild {guild_id}...")
            
            # Specific migrations with existence checks
            migrations = [
                ("current_round", "ALTER TABLE tournaments ADD COLUMN current_round INT DEFAULT 1"),
                ("teams_remaining", "ALTER TABLE tournaments ADD COLUMN teams_remaining INT DEFAULT 0"),
                ("completed_at", "ALTER TABLE tournaments ADD COLUMN completed_at TIMESTAMP NULL")
            ]
            
            for column_name, alter_sql in migrations:
                try:
                    # Check if column exists
                    check_query = f"""
                    SELECT COUNT(*) as col_exists FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'tournaments' AND COLUMN_NAME = '{column_name}'
                    """
                    
                    result = db_connection.fetch_one(guild_id, check_query)
                    
                    if result and result['col_exists'] == 0:
                        # Column doesn't exist, add it
                        db_connection.execute_query(guild_id, alter_sql)
                        print(f"   ✅ Columna '{column_name}' añadida a tabla tournaments")
                        success_count += 1
                    else:
                        print(f"   ℹ️ Columna '{column_name}' ya existe en tabla tournaments")
                        success_count += 1
                        
                except Exception as e:
                    print(f"   ❌ Error añadiendo columna '{column_name}': {e}")
                    error_count += 1
            
            # Fix game_id column type in tournament_matches
            try:
                db_connection.execute_query(guild_id, "ALTER TABLE tournament_matches MODIFY COLUMN game_id BIGINT NULL")
                print("   ✅ Tipo de columna game_id actualizado en tournament_matches")
                success_count += 1
            except Exception as e:
                if "doesn't exist" not in str(e):
                    print(f"   ⚠️ Error actualizando tipo de columna game_id: {e}")
                    error_count += 1
                else:
                    print("   ℹ️ Tabla tournament_matches no existe o ya está actualizada")
                    success_count += 1
            
            print(f"✅ Migración completada: {success_count} exitosas, {error_count} errores")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            error_count += 1
        
        return success_count, error_count

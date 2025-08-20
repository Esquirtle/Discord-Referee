
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env'))

class Config:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.command_prefix = os.getenv("COMMAND_PREFIX", ".")
        self.description = "A Discord bot for managing matches, tournaments, and leagues."
        self.database_url = os.getenv("DATABASE_URL")
        self.languages = ["en", "es", "fr"]
        self.default_language = "en"
        self.log_level = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    def getToken(self):
        return str(self.token)
    def getCommandPrefix(self):
        return str(self.command_prefix)
    def getDescription(self):
        return str(self.description)
    def getDatabaseUrl(self):
        return str(self.database_url)
    def getLanguages(self):
        return [str(lang) for lang in self.languages]
    def getDefaultLanguage(self):
        return str(self.default_language)
    def getLogLevel(self):
        return str(self.log_level)
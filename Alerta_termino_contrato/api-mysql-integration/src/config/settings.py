import os

class Settings:
    def __init__(self):
        self.load_env_variables()

    def load_env_variables(self):
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "3306")
        self.DB_USER = os.getenv("DB_USER", "root")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        self.DB_NAME = os.getenv("DB_NAME", "my_database")
        self.API_URL = os.getenv("API_URL", "https://example.com/api")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
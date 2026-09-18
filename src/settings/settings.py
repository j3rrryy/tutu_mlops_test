import os


class Settings:
    APP_NAME = os.environ["APP_NAME"]
    VERSION = os.environ["VERSION"]
    DEBUG = bool(int(os.environ["DEBUG"]))

    POSTGRES_DRIVER = "postgresql+asyncpg"
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = int(os.environ["POSTGRES_PORT"])

    MODEL_PATH = os.environ["MODEL_PATH"]
    MODEL_METADATA_PATH = os.environ["MODEL_METADATA_PATH"]
    FEATURES_PATH = os.environ["FEATURES_PATH"]

    HOST = "0.0.0.0"
    PORT = 8000
    WORKERS = 3
    LIMIT_MAX_REQUESTS = 50000

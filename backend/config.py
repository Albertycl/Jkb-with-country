import os


class Config:
    SECRET_KEY = os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ENABLE_POLLERS = os.environ.get("ENABLE_POLLERS", "false").lower() == "true"
    JKB_USER_EMAIL = os.environ.get("JKB_USER_EMAIL", "")
    JKB_USER_PWD = os.environ.get("JKB_USER_PWD", "")
    JKB_CLIENT_ID = os.environ.get("JKB_CLIENT_ID", "")
    JKB_CLIENT_SECRET = os.environ.get("JKB_CLIENT_SECRET", "")
    CEDEXIS_TOKEN = os.environ.get("CEDEXIS_TOKEN", "")
    INFRA_LOOKUP_URL = os.environ.get("INFRA_LOOKUP_URL", "")


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True

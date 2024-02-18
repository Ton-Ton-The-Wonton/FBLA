"""configs"""

import logging


class Config:
    PORT = 5003
    SQLALCHEMY_DATABASE_URI = "sqlite:///"


class DevConfig(Config):
    """DevConfig"""

    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProdConfig(Config):
    """ProdConfig"""

    DEBUG = False
    LOG_LEVEL = logging.INFO

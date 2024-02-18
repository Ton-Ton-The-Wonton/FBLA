"""config package"""

from os import environ
from configs.configs import DevConfig, ProdConfig

PROFILE = environ.get("env", "dev")

if PROFILE == "prod":
    Config = ProdConfig
elif PROFILE == "dev":
    Config = DevConfig

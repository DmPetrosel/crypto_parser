config = {
    "project": {
        "name": "crypto_parser",
    }
}
from configparser import ConfigParser

config = ConfigParser()

config.read("config.ini")


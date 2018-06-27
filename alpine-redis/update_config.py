from walkoff.config import Config

Config.load_config("data/walkoff.config")
Config.CACHE = {
    "type": "redis",
    "host": "172.17.0.3",
    "port": 6379
}
Config.HOST = "0.0.0.0"
Config.write_values_to_file()

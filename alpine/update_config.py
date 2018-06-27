from walkoff.config import Config

Config.load_config("data/walkoff.config")
Config.HOST = "0.0.0.0"
Config.write_values_to_file()

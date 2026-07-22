from src.config.configuration import ConfigurationManager

config = ConfigurationManager()

print(type(config.config))
print(config.config)
print(config.get_data_ingestion_config())
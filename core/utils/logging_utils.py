import logging
import logging.config
import yaml

def setup_logging(config_path='config/logging.conf'):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

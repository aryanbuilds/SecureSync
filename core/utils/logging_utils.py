import logging
import logging.config
import os

class ScannerLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self._configure_logger()

    def _configure_logger(self):
        config_path = 'config/logging.conf'
        if os.path.exists(config_path):
            logging.config.fileConfig(config_path)
        else:
            logging.basicConfig(level=logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
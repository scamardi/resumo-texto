import logging.config
from pythonjsonlogger import jsonlogger

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["stdout", "file"],
            "level": "DEBUG",
        },
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING)

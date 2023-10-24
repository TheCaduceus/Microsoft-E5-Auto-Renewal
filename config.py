from os import environ as env

"""
Changing value to "" (empty) or 0 will force the program to acquire that variable's value from system environment.
"""

REFRESH_TOKEN = "" or env.get("E5_REFRESH_TOKEN")
CLIENT_ID = "" or env.get("E5_CLIENT_ID")
CLIENT_SECRET = "" or env.get("E5_CLIENT_SECRET")
WEB_APP_PASSWORD = "" or env.get("E5_WEB_APP_PASSWORD")
WEB_APP_HOST = "0.0.0.0" or env.get("E5_WEB_APP_HOST")
WEB_APP_PORT = int(env.get("PORT", 8080))
TIME_DELAY = int(env.get("E5_TIME_DELAY", 3))

# WEB SERVER LOGGING CONFIGURATION
LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'event-log.txt',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'uvicorn.error': {
            'level': 'WARNING',
            'handlers': ['file_handler', 'stream_handler']
        },
        'httpx': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}

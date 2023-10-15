from os import environ as env

"""
Changing value to "" (empty) or 0 will force the program to acquire that variable's value from system environment.
"""

REFRESH_TOKEN = "" or env.get("E5_REFRESH_TOKEN")
CLIENT_ID = "" or env.get("E5_CLIENT_ID")
CLIENT_SECRET = "" or env.get("E5_CLIENT_SECRET")
WEB_APP_PASSWORD = "" or env.get("E5_WEB_APP_PASSWORD")
WEB_APP_HOST = "0.0.0.0" or env.get("E5_WEB_APP_HOST")
WEB_APP_PORT = int(env.get("PORT"))
TIME_DELAY = 3 or int(env.get("E5_TIME_DELAY"))

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
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['stream_handler']
    }
}

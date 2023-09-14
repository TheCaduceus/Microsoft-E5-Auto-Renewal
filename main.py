from flask import Flask, request
from threading import Thread
from time import sleep
from httpx import Client as httpx_client
from random import shuffle
from logging import (
    getLogger, 
    basicConfig,
    FileHandler, 
    StreamHandler,
    INFO
)

from config import (
    REFRESH_TOKEN,
    CLIENT_ID,
    CLIENT_SECRET,
    WEB_APP_PASSWORD,
    WEB_APP_HOST,
    WEB_APP_PORT,
    TIME_DELAY
)

basicConfig(
    level=INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s",
    handlers=[FileHandler('event-log.txt'), StreamHandler()]
)
logger = getLogger('server')

web_app = Flask(__name__)
web_client = httpx_client()

auth_endpoint= "https://login.microsoftonline.com/common/oauth2/v2.0/token"
endpoints = [
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
    'https://graph.microsoft.com/v1.0/applications?$count=true',
    'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/beta/me/outlook/masterCategories',
    'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
    'https://graph.microsoft.com/v1.0/sites/root/lists',
    'https://graph.microsoft.com/v1.0/sites/root',
    'https://graph.microsoft.com/v1.0/sites/root/drives'
]

def acquire_access_token() -> str:
    """
    Acquires the access token for the web client by making a POST request to the authentication endpoint with the provided data.

    Returns:
        The access token.
    """
    web_client.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }
    return web_client.post(auth_endpoint, data=data).json()['access_token']

def call_endpoints() -> None:
    shuffle(endpoints)
    web_client.headers.update(
        {
            'Authorization': acquire_access_token(),
            'Content-Type': 'application/json'
        }
    )

    for endpoint in endpoints:
        sleep(TIME_DELAY)
        try:
            web_client.get(endpoint)
        except Exception:
            pass

@web_app.route("/")
def home():
    return 'Server is up!'

@web_app.errorhandler(400)
def invalid_request(e):
  return 'Invalid request.'

@web_app.errorhandler(404)
def not_found(e):
  return 'Resource not found.'

@web_app.errorhandler(405)
def invalid_method(e):
  return 'Invalid method.'

@web_app.errorhandler(415)
def no_data(e):
   return 'No json data passed.'

@web_app.route('/call', methods=['POST'])
def run_executor() -> str:
    json_data = request.json
    if 'password' not in json_data.keys():
       return 'Password is required to use web app.'
    if json_data['password'] != WEB_APP_PASSWORD:
       return 'Access denied - invalid password.'
    executor = Thread(target=call_endpoints)
    executor.start()
    return 'Success.'

if __name__ == '__main__':
  web_app.run(host=WEB_APP_HOST, port=WEB_APP_PORT)

from flask import Flask, request, Response, send_file
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
    datefmt='%d/%m/%Y %H:%M:%S',
    format='[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
    handlers=[FileHandler('event-log.txt'), StreamHandler()]
)
logger = getLogger('server')

web_server = Flask(__name__)
web_client = httpx_client()

auth_endpoint= 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
server_stats = {'version': 1.2,'totalRequests': 0, 'totalSuccess': 0, 'totalErrors': 0 }
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

def acquire_access_token(refresh_token:str|None=None) -> str:
    """
    Acquires the access token for the web client by making a POST request to the authentication endpoint with the provided data.

    Args:
        refresh_token (str | None): The refresh token used to acquire the access token. If None, the default refresh token will be used.

    Returns:
        str: The access token.
    """
    web_client.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token or REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }

    return web_client.post(auth_endpoint, data=data).json()['access_token']

def call_endpoints(access_token:str) -> None:
    """
    Shuffles the endpoints list, updates the headers of the web client with the provided access token, and makes GET requests to each endpoint in the shuffled list with a delay between each request.

    Args:
        access_token (str): The access token used for authorization.

    Returns:
        None
    """
    shuffle(endpoints)
    web_client.headers.update(
        {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
    )

    for endpoint in endpoints:
        sleep(TIME_DELAY)
        try:
            web_client.get(endpoint)
        except Exception:
            pass

@web_server.route("/")
def home() -> Response:
    return server_stats, 200

@web_server.after_request
def requests_counter(response:Response):
    server_stats['totalRequests'] += 1
    if response.status_code == 201:
        server_stats['totalSuccess'] += 1
    elif response.status_code >= 400:
        server_stats['totalErrors'] += 1
    return response

@web_server.errorhandler(400)
def invalid_request(_) -> Response:
    return 'Invalid request.', 400

@web_server.errorhandler(404)
def not_found(_) -> Response:
    return 'Resource not found.', 404

@web_server.errorhandler(405)
def invalid_method(_) -> Response:
    return 'Invalid method.', 405

@web_server.errorhandler(415)
def no_data(_) -> Response:
    return 'No json data passed.', 415

@web_server.route('/call', methods=['POST'])
def run_executor() -> Response:
    json_data = request.json
    password = json_data.get('password')
    if not password:
        return 'Password is required to use web app.', 401
    if password != WEB_APP_PASSWORD:
        return 'Access denied - invalid password.', 403
    
    refresh_token = json_data.get('refresh_token')
    access_token = acquire_access_token(refresh_token)
    
    executor = Thread(target=call_endpoints, args=[access_token])
    executor.start()
    
    return 'Success - new thread created.', 201

@web_server.route('/getLog')
def send_logs() -> Response:
    password = request.args.get('password')
    if not password:
        return 'Password is required to download log file.', 401
    if password != WEB_APP_PASSWORD:
        return 'Access denied - invalid password.', 403
    
    return send_file('event-log.txt')

if __name__ == '__main__':
    web_server.run(host=WEB_APP_HOST, port=WEB_APP_PORT)

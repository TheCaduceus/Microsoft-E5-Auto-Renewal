from flask import Flask, request, redirect, Response
from sys import argv, exit as sexit
from httpx import Client as httpx_client
from webbrowser import open as open_link
from logging import (
    getLogger,
    basicConfig,
    FileHandler,
    StreamHandler,
    INFO,
    WARNING
)

basicConfig(
    level=INFO,
    datefmt='%d/%m/%Y %H:%M:%S',
    format='[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
    handlers=[FileHandler('event-log.txt'), StreamHandler()]
)
logger = getLogger('auth_client')
getLogger('werkzeug').setLevel(WARNING)

if len(argv) < 3:
    logger.error("Error: You must pass both the client ID and secret as command line arguments.")
    sexit(1)

SCOPES = [
    "Directory.Read.All",
    "Directory.ReadWrite.All",
    "Files.Read",
    "Files.Read.All",
    "Files.ReadWrite",
    "Files.ReadWrite.All",
    "Mail.Read",
    "Mail.ReadWrite",
    "MailboxSettings.Read",
    "MailboxSettings.ReadWrite",
    "offline_access",
    "Sites.Read.All",
    "Sites.ReadWrite.All",
    "User.Read",
    "User.Read.All",
    "User.ReadWrite.All"
]
auth_endpoint = (
    'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    f'?client_id={argv[1]}'
    '&response_type=code'
    '&redirect_uri=http://localhost:53682'
    f'&scope={"+".join(SCOPES)}'
)
token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

web_server = Flask('auth_client')
web_client = httpx_client()

@web_server.errorhandler(400)
def invalid_request(_=None) -> Response:
    return 'Invalid request.', 400

@web_server.errorhandler(404)
def not_found(_) -> Response:
    return 'Resource not found.', 404

@web_server.route('/')
def callback() -> Response:
    code = request.args.get('code', None)
    if not code:
        return invalid_request()
    
    resp = web_client.post(token_url, data={
        'client_id': argv[1],
        'client_secret': argv[2],
        'code': code,
        'redirect_uri': "http://localhost:53682",
        'grant_type': 'authorization_code'
    }).json()
    logger.info(resp)
    
    return resp, 200

@web_server.route('/auth')
def auth() -> Response:
    return redirect(auth_endpoint)
    

if __name__ == '__main__':
    logger.info('If your browser does not open automatically go to the following link: http://127.0.0.1:53682/auth')
    open_link('http://127.0.0.1:53682/auth', 1)
    web_server.run(host='0.0.0.0', port=53682)

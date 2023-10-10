import uvicorn

from quart import Quart, request, redirect, Response
from sys import argv, exit as sys_exit
from httpx import AsyncClient as httpx_client
from webbrowser import open as open_link
from logging import getLogger

from config import LOGGER_CONFIG_JSON

if len(argv) < 3:
    print("Error: You must pass both the client ID and secret as command line arguments.")
    sys_exit(1)

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

web_server = Quart('auth_client')
web_client = httpx_client()

@web_server.before_serving
async def before_serve() -> None:
    logger = getLogger('uvicorn')
    logger.info('If your browser does not open automatically go to the following link:\nhttp://127.0.0.1:53682/auth')
    open_link('http://127.0.0.1:53682/auth', new=1)

@web_server.errorhandler(400)
async def invalid_request(_=None) -> Response:
    return 'Invalid request.', 400

@web_server.errorhandler(404)
async def not_found(_) -> Response:
    return 'Resource not found.', 404

@web_server.route('/')
async def callback() -> Response:
    code = request.args.get('code', None)
    if not code:
        return await invalid_request()
    
    resp = (await web_client.post(token_url, data={
        'client_id': argv[1],
        'client_secret': argv[2],
        'code': code,
        'redirect_uri': "http://localhost:53682",
        'grant_type': 'authorization_code'
    })).json()
    
    return resp, 200

@web_server.route('/auth')
async def auth() -> Response:
    return redirect(auth_endpoint)
    
if __name__ == '__main__':
    uvicorn.run(
        app=web_server,
        host='0.0.0.0',
        port=53682,
        log_config=LOGGER_CONFIG_JSON,
        access_log=False
    )

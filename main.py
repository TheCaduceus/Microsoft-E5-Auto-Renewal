from uvicorn import run
from quart import (
    Quart,
    request,
    Response as quartResponse,
    send_file,
    abort
)
from werkzeug.exceptions import HTTPException
from asyncio import sleep as async_sleep
from httpx import AsyncClient as httpx_client, Response as httpxResponse
from random import shuffle
from logging import getLogger

from config import (
    REFRESH_TOKEN,
    CLIENT_ID,
    CLIENT_SECRET,
    WEB_APP_PASSWORD,
    WEB_APP_HOST,
    WEB_APP_PORT,
    TIME_DELAY,
    LOGGER_CONFIG_JSON
)

web_server = Quart(__name__)
web_client = httpx_client()

server_stats = {'version': 1.7,'totalRequests': 0, 'totalSuccess': 0, 'totalErrors': 0}
token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
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

async def log_response(response:httpxResponse) -> None:
    request = response.request
    logger.info(f'HTTP Request: {request.method} {request.url} {response.http_version} {response.status_code} {response.reason_phrase}')

async def acquire_access_token(refresh_token:str|None=None) -> str:
    web_client.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token or REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:53682/'
    }

    return (await web_client.post(token_endpoint, data=data)).json().get('access_token') or abort(401, "Failed to acquire the access token. Please verify your refresh token and try again.")

async def call_endpoints(access_token:str) -> None:
    shuffle(endpoints)
    web_client.headers.update(
        {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }
    )

    for endpoint in endpoints:
        await async_sleep(TIME_DELAY)
        try:
            await web_client.get(endpoint)
        except Exception:
            pass

@web_server.before_serving
async def before_serve() -> None:
    global logger
    logger = getLogger('uvicorn')
    web_client.event_hooks['response'] = [log_response]
    logger.info("Server is now started!")
    host = f"127.0.0.1:{WEB_APP_PORT}" if WEB_APP_HOST == "0.0.0.0" else f"{WEB_APP_HOST}:{WEB_APP_PORT}"
    logger.info(f'Server running on {host}')

@web_server.after_serving
async def after_serve() -> None:
    logger.info('Server is now stopped!')

@web_server.before_request
async def before_request() -> None:
    server_stats['totalRequests'] += 1

@web_server.after_request
async def after_request(response:quartResponse) -> quartResponse:
    if response.status_code == 201:
        server_stats['totalSuccess'] += 1
    elif response.status_code >= 400:
        server_stats['totalErrors'] += 1
    return response

@web_server.errorhandler(400)
async def invalid_request(_) -> quartResponse:
    return 'Invalid request.', 400

@web_server.errorhandler(401)
async def authentication_required(error:HTTPException) -> quartResponse:
    return error.description or 'Password is required to use this route.', 401

@web_server.errorhandler(403)
async def access_denied(_) -> quartResponse:
    return 'Access denied - invalid password.', 403

@web_server.errorhandler(404)
async def not_found(_) -> quartResponse:
    return 'Resource not found.', 404

@web_server.errorhandler(405)
async def invalid_method(_) -> quartResponse:
    return 'Invalid method.', 405

@web_server.errorhandler(415)
async def no_data(_) -> quartResponse:
    return 'No json data passed.', 415

@web_server.route("/")
async def home() -> quartResponse:
    return server_stats, 200

@web_server.route('/call', methods=['POST'])
async def create_task() -> quartResponse:
    json_data = await request.json or abort(415)
    password = json_data.get('password') or abort(401, None)
    if password != WEB_APP_PASSWORD:
        abort(403)
    
    refresh_token = json_data.get('refresh_token')
    access_token = await acquire_access_token(refresh_token)

    web_server.add_background_task(call_endpoints, access_token)
    
    return 'Success - new task created.', 201

"""
@web_server.route('/logs')
async def send_logs() -> quartResponse:
    password = request.args.get('password') or abort(401, None)
    as_file = request.args.get('as_file', 'False') in {'TRUE','True','true'}
    if password != WEB_APP_PASSWORD:
        abort(403)
    
    return await send_file('event-log.txt', as_attachment=as_file)
"""

if __name__ == '__main__':
    run(
        app="main:web_server",
        host=WEB_APP_HOST,
        port=WEB_APP_PORT,
        log_config=LOGGER_CONFIG_JSON,
        access_log=False
    )

from uvicorn import run
from quart import Quart, request, Response as quartResponse, send_file
from httpx import AsyncClient as httpx_client
from asyncio import sleep as async_sleep
from random import shuffle
from logging import getLogger
from config import *

class WebServer:
    instance = Quart(__name__)
    version = 2.1
    stats = {'version': version, 'totalRequests': 0, 'totalSuccess': 0, 'totalErrors': 0}

    def __init__(self):
        self.logger = getLogger('uvicorn')

        @self.instance.before_serving
        async def before_serve():
            host = f"127.0.0.1:{WEB_APP_PORT}" if WEB_APP_HOST == "0.0.0.0" else f"{WEB_APP_HOST}:{WEB_APP_PORT}"
            self.logger.info(f'Server running on {host}')

        @self.instance.after_serving
        async def after_serve():
            self.logger.info('Server is now stopped!')

        @self.instance.before_request
        async def before_request():
            self.stats['totalRequests'] += 1

        @self.instance.after_request
        async def after_request(response: quartResponse):
            if response.status_code == 201:
                self.stats['totalSuccess'] += 1
            elif response.status_code >= 401:
                self.stats['totalErrors'] += 1

            return response
        
        ErrorHandler(self.instance)
        RouteHandler(self.instance)

class HTTPError(Exception):
    status_code:int = None
    description:str = None
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description
        super().__init__(self.status_code, self.description)

class ErrorHandler:
    def __init__(self, instance: Quart):
        self.error_messages =  {
            400: 'Invalid request.',
            401: 'Password is required to use this route.',
            403: 'Access denied - invalid password.',
            404: 'Resource not found.',
            405: 'Invalid method',
            415: 'No json data passed.'
        }

        @instance.errorhandler(400)
        async def invalid_request(_):
            return 'Invalid request.', 400
        
        @instance.errorhandler(404)
        async def not_found(_):
            return 'Resource not found.', 404
        
        @instance.errorhandler(405)
        async def invalid_method(_):
            return 'Invalid request method.', 405
        
        @instance.errorhandler(HTTPError)
        async def http_error(error:HTTPError):
            error_message = self.error_messages[error.status_code]
            return error.description or error_message, error.status_code

    @classmethod
    def abort(cls, status_code:int = 500, description:str = None):
        raise HTTPError(status_code, description)

class RouteHandler:
    def __init__(self, instance: Quart):
    
        @instance.route('/')
        async def home():
            return WebServer.stats, 200

        @instance.route('/call', methods=['POST'])
        async def create_task():
            json_data = await request.json or ErrorHandler.abort(415)
            password = json_data.get('password') or ErrorHandler.abort(401)

            if password != WEB_APP_PASSWORD:
                ErrorHandler.abort(403)
            
            refresh_token = json_data.get('refresh_token')
            client_id = json_data.get('client_id')
            client_secret = json_data.get('client_secret')
            access_token = await HTTPClient.acquire_access_token(refresh_token, client_id, client_secret)

            instance.add_background_task(HTTPClient.call_endpoints, access_token)

            return 'Success - new task created.', 201
        
        @instance.route('/logs')
        async def send_logs():
            password = request.args.get('password') or ErrorHandler.abort(401)
            as_file = request.args.get('as_file', 'False') in {'TRUE', 'True', 'true'}

            if password != WEB_APP_PASSWORD:
                ErrorHandler.abort(403)

            return await send_file('event-log.txt', as_attachment=as_file)

class HTTPClient:
    instance = httpx_client()
    token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    graph_endpoints = [
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

    @classmethod
    async def acquire_access_token(
        cls,
        refresh_token:str = None,
        client_id:str = None,
        client_secret:str = None
    ):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token or REFRESH_TOKEN,
            'client_id': client_id or CLIENT_ID,
            'client_secret': client_secret or CLIENT_SECRET,
            'redirect_uri': 'http://localhost:53682/'
        }

        response = await cls.instance.post(cls.token_endpoint, headers=headers, data=data)
        return response.json().get('access_token') or ErrorHandler.abort(
            401,
            'Failed to acquire the access token. Please verify your refresh token and try again.'
        )
    
    @classmethod
    async def call_endpoints(cls, access_token:str):
        shuffle(cls.graph_endpoints)
        headers = {
            'Authorization': access_token,
            'Content-Type': 'application/json'
        }

        for endpoint in cls.graph_endpoints:
            await async_sleep(TIME_DELAY)
            try:
                await cls.instance.get(endpoint, headers=headers)
            except Exception:
                pass

web_server = WebServer().instance

if __name__ == '__main__':
    run(
        app="main:web_server",
        host=WEB_APP_HOST,
        port=WEB_APP_PORT,
        log_config=LOGGER_CONFIG_JSON,
        access_log=False
    )

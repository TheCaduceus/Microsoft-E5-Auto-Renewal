from uvicorn import run
from quart import Quart, request, redirect
from httpx import AsyncClient as httpx_client
from sys import argv, exit as sys_exit
from webbrowser import open as open_link
from logging import getLogger
from config import LOGGER_CONFIG_JSON

class WebServer:
    instance = Quart(__name__)
    scopes = [
        'Directory.Read.All',
        'Directory.ReadWrite.All',
        'Files.Read',
        'Files.Read.All',
        'Files.ReadWrite',
        'Files.ReadWrite.All',
        'Mail.Read',
        'Mail.ReadWrite',
        'MailboxSettings.Read',
        'MailboxSettings.ReadWrite',
        'offline_access',
        'Sites.Read.All',
        'Sites.ReadWrite.All',
        'User.Read',
        'User.Read.All',
        'User.ReadWrite.All'
    ]
    auth_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    auth_redirect_url = 'http://localhost:53682'

    def __init__(self):
        self.logger = getLogger('uvicorn')

        @self.instance.before_serving
        async def before_serve():
            self.logger.info(f'If your browser does not open automatically go to the following link:\n{self.auth_redirect_url}')
            open_link(self.auth_redirect_url, new=1)

        @self.instance.after_serving
        async def after_serve():
            self.logger.info('Server is not stopped!')

        ErrorHandler(self.instance)
        RouteHandler(self.instance)

class HTTPError(Exception):
    status_code: int = None
    description: str = None

    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description
        super().__init__(self.status_code, self.description)

class ErrorHandler:
    def __init__(self, instance: Quart):
        self.error_messages = {
            400: 'Invalid request.',
            500: 'Internal server error.'
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
        async def http_error(error: HTTPError):
            error_message = self.error_messages[error.status_code]
            return error.description or error_message, error.status_code

    @classmethod
    def abort(cls, status_code: int = 500, description: str = None):
        raise HTTPError(status_code, description)

class RouteHandler:
    def __init__(
        self,
        instance: Quart,
    ):
        self.authorization_url = (
            f'{WebServer.auth_endpoint}'
            f'?client_id={argv[1]}'
            '&response_type=code'
            f'&redirect_uri={WebServer.auth_redirect_url}'
            f'&scope={"+".join(WebServer.scopes)}'
        )
        @instance.route('/')
        async def root():
            code = request.args.get('code')

            if code:
                return (await HTTPClient.redeem_auth_code(code)), 200

            return redirect(self.authorization_url)

class HTTPClient:
    instance = httpx_client()
    token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

    @classmethod
    async def redeem_auth_code(
        cls,
        code: str,
        client_id: str = argv[1],
        client_secret: str = argv[2]
    ):
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': WebServer.auth_redirect_url,
            'code': code
        }

        return (await cls.instance.post(cls.token_url, data=data)).json()

web_server = WebServer().instance

if __name__ == '__main__':

    if len(argv) < 3:
        print('Error: You must pass both the client ID and secret as command line arguments.')
        sys_exit(1)

    run(
        app='auth:web_server',
        host="0.0.0.0",
        port=53682,
        log_config=LOGGER_CONFIG_JSON,
        access_log=False
    )

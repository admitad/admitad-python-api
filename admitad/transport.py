import json
import logging
from base64 import b64encode
from typing import ClassVar, Literal

import requests

from admitad.constants import (
    DEFAULT_PAGINATION_LIMIT,
    DEFAULT_PAGINATION_OFFSET,
    DEFAULT_REQUEST_TIMEOUT,
    MAX_PAGINATION_LIMIT,
    TOKEN_URL,
)
from admitad.exceptions import HttpException, ConnectionException, JsonException

LOG = logging.getLogger(__file__)
LOG.addHandler(logging.StreamHandler())


def to_json(content: str | bytes | bytearray) -> dict:
    try:
        return json.loads(content)
    except (TypeError, ValueError):
        return content


def debug_log(value: str, debug: bool = True) -> None:
    if debug:
        LOG.setLevel(logging.DEBUG)
        LOG.debug(value)
    else:
        LOG.setLevel(logging.NOTSET)


def get_credentials(client_id: str, client_secret: str) -> str:
    return b64encode(
        ('%s:%s' % (client_id, client_secret)).encode('utf-8')
    ).decode('utf-8')


def build_headers(access_token: str, user_agent: str | None = None) -> dict:
    headers = {
        'Authorization': 'Bearer %s' % access_token,
        'Connection': 'Keep-Alive',
    }

    if user_agent:
        headers['User-Agent'] = user_agent
    return headers


def prepare_data(data: dict | None = None) -> dict | None:
    if data:
        new_data = {}
        for key, value in data.items():
            if isinstance(value, (list, tuple, set)):
                new_data[key] = [item for item in value if item is not None]
            else:
                new_data[key] = value if value is not None else None
        return new_data
    return data


def prepare_request_data(
    data: dict | None = None,
    headers: dict | None = None,
    method: Literal['GET', 'POST', 'DELETE', 'PUT'] = 'GET',
    timeout: int | None = None,
    ssl_verify: bool = False,
) -> dict:
    kwargs = {
        'headers': headers if headers is not None else {},
        'timeout': timeout if timeout is not None else DEFAULT_REQUEST_TIMEOUT,
        'verify': ssl_verify,
        'allow_redirects': True,
    }

    prepared_data = prepare_data(data)

    if method in ['POST', 'PUT']:
        kwargs['data'] = prepared_data
    if method in ['GET', 'DELETE']:
        kwargs['params'] = prepared_data

    return kwargs


def api_request(
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
    method: Literal['GET', 'POST', 'DELETE', 'PUT'] = 'GET',
    files: dict | None = None,
    timeout: int | None = None,
    ssl_verify: bool = True,
    debug: bool = False,
) -> dict:
    kwargs = prepare_request_data(
        data=data,
        headers=headers,
        method=method,
        timeout=timeout,
        ssl_verify=ssl_verify,
    )
    status_code = 500
    content = ''
    try:
        response = requests.request(method, url, files=files, **kwargs)
        debug_log('Request url: %s' % response.url, debug)
        # if method == 'POST':
        #     debug_log('Request body: %s' % response.request.body, debug)
        status_code = response.status_code
        content = response.content
        response.raise_for_status()
    except requests.HTTPError as err:
        raise HttpException(status_code, to_json(content), err)
    except requests.RequestException as err:
        raise ConnectionException(err)
    except (ValueError, TypeError) as err:
        raise JsonException(err)
    return response.json()

def oauth_refresh_access_token(data: dict) -> dict:
    """
    refresh an access token. Returns dictionary with new access_token.
    data['access-token']
    The function parameter should be a dictionary with next structure:
    data = {
        'refresh_token': '',
        'client_secret': '',
        'client_id': ''
    }
    """
    refresh_token = data['refresh_token']
    client_id = data['client_id']
    client_secret = data['client_secret']
    params = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return api_request(
        url=TOKEN_URL,
        method='POST',
        data=params,
        headers=headers,
    )


def oauth_client_authorization(data: dict) -> dict:
    """
    OAuth2 client authorization.
    Used to get an access_token with the oauth client credentials
    The function parameter should be a dictionary with next structure:
    data = {
        'client_secret': '',
        'client_id': ''
        'scopes': '',
    }
    """
    client_id = data['client_id']
    client_secret = data['client_secret']
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'scope': data['scopes']
    }
    credentials = get_credentials(client_id, client_secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic %s' % credentials
    }
    return api_request(
        url=TOKEN_URL,
        method='POST',
        data=params,
        headers=headers,
    )


class HttpTransport:
    SUPPORTED_METHODS: ClassVar[tuple[Literal['GET', 'POST', 'DELETE', 'PUT']]] = ('GET', 'POST', 'DELETE', 'PUT')

    def __init__(
        self,
        access_token: str,
        user_agent: str | None = None,
        debug: bool = False,
    ):
        self._headers = build_headers(access_token, user_agent=user_agent)
        self._method = 'GET'
        self._files = None
        self._data = None
        self._url = None
        self._debug = debug

    def set_method(self, method: Literal['GET', 'POST', 'DELETE', 'PUT']) -> 'HttpTransport':
        if method in self.SUPPORTED_METHODS:
            self._method = method
        else:
            raise AttributeError('This http method "%s" is not supported' % method)
        # here we should clean data
        return self.clean_data()

    def get(self) -> 'HttpTransport':
        return self.set_method('GET')

    def post(self) -> 'HttpTransport':
        return self.set_method('POST')

    def put(self) -> 'HttpTransport':
        return self.set_method('PUT')

    def delete(self) -> 'HttpTransport':
        return self.set_method('DELETE')

    def set_debug(self, debug: bool) -> 'HttpTransport':
        self._debug = debug
        return self

    def set_url(self, url: str, **kwargs: dict) -> 'HttpTransport':
        self._url = url % kwargs
        return self

    def set_data(self, data: dict) -> 'HttpTransport':
        self._data = data
        return self

    def clean_data(self) -> 'HttpTransport':
        self._data = None
        return self

    def update_data(self, values: dict | None) -> 'HttpTransport':
        if self._data is None:
            self._data = {}
        self._data.update(values)
        return self

    def set_files(self, files) -> 'HttpTransport':
        self._files = files
        return self

    def set_pagination(self, **kwargs) -> 'HttpTransport':
        limit = kwargs.get('limit', DEFAULT_PAGINATION_LIMIT)
        offset = kwargs.get('offset', DEFAULT_PAGINATION_OFFSET)

        data = {
            'limit': limit if 0 < limit <= MAX_PAGINATION_LIMIT else DEFAULT_PAGINATION_LIMIT,
            'offset': offset if offset > 0 else DEFAULT_PAGINATION_OFFSET,
        }

        return self.update_data(data)

    def set_ordering(self, ordering) -> 'HttpTransport':
        order_by = ordering.get('order_by', [])
        available = ordering.get('available', [])

        if not isinstance(order_by, (list, tuple, set)):
            order_by = [order_by]

        data = {
            'order_by': [item for item in order_by if item is not None and
                         (item[1:] if item[0] == '-' else item) in available]
        }

        return self.update_data(data)

    def set_filtering(self, filtering) -> 'HttpTransport':
        filter_by = filtering.get('filter_by', {})
        available = filtering.get('available', {})

        data = {key: available[key](value) for key, value in filter_by.items() if key in available}

        return self.update_data(data)

    def request(self, **kwargs: dict) -> dict:
        if 'url' in kwargs:
            self.set_url(kwargs.pop('url'), **kwargs)
        if 'debug' in kwargs:
            self.set_debug(kwargs.pop('debug'))
        if not self._url:
            raise AttributeError(
                'Absent url parameter. Use set_url method or pass '
                'url parameter in this method.'
            )

        response = HttpTransport.api_request(
            url=self._url,
            method=self._method,
            headers=self._headers,
            data=self._data,
            debug=self._debug,
            files=self._files,
        )
        handler = kwargs.get('handler', self._handle_response)

        return handler(response)

    @staticmethod
    def api_request(
        url: str,
        method: Literal['GET', 'POST', 'DELETE', 'PUT'],
        headers: dict | None = None,
        data: dict | None = None,
        debug: bool = False,
        files: dict | None = None,
        **kwargs: dict,
    ) -> dict:
        return api_request(
            url=url,
            method=method,
            headers=headers,
            data=data,
            debug=debug,
            files=files,
            **kwargs,
        )

    @staticmethod
    def _handle_response(response: dict) -> dict:
        return response

    def __call__(self, **kwargs: dict) -> dict:
        return self.request(**kwargs)

# coding: utf-8
from __future__ import unicode_literals

import json
import logging
from base64 import b64encode

import requests

from pyadmitad.constants import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET, \
    DEFAULT_REQUEST_TIMEOUT, MAX_PAGINATION_LIMIT, TOKEN_URL
from pyadmitad.exceptions import HttpException, ConnectionException, JsonException

LOG = logging.getLogger(__file__)
LOG.addHandler(logging.StreamHandler())


def to_json(content):
    try:
        return json.loads(content)
    except (TypeError, ValueError):
        return content


def debug_log(value, debug=True):
    if debug:
        LOG.setLevel(logging.DEBUG)
        LOG.debug(value)
    else:
        LOG.setLevel(logging.NOTSET)


def get_credentials(client_id, client_secret):
    return b64encode(
        ('%s:%s' % (client_id, client_secret)).encode('utf-8')
    ).decode('utf-8')


def build_headers(access_token, user_agent=None):
    headers = {
        'Authorization': 'Bearer %s' % access_token,
        'Connection': 'Keep-Alive',
    }

    if user_agent:
        headers['User-Agent'] = user_agent
    return headers


def prepare_data(data=None):
    if data:
        new_data = {}
        for key, value in data.items():
            if isinstance(value, (list, tuple, set)):
                new_data[key] = [item for item in value if item is not None]
            else:
                new_data[key] = value if value is not None else None
        return new_data
    return data


def prepare_request_data(data=None, headers=None, method='GET',
                         timeout=None, ssl_verify=False):
    kwargs = {
        'headers': headers if headers is not None else {},
        'timeout': timeout if timeout is not None else DEFAULT_REQUEST_TIMEOUT,
        'verify': ssl_verify,
        'allow_redirects': True,
    }

    prepared_data = prepare_data(data)

    if method == 'POST':
        kwargs['data'] = prepared_data
    if method == 'GET':
        kwargs['params'] = prepared_data

    return kwargs


def api_request(url, data=None, headers=None, method='GET',
                files=None, timeout=None, ssl_verify=True, debug=False):
    kwargs = prepare_request_data(data=data, headers=headers, method=method,
                                  timeout=timeout, ssl_verify=ssl_verify)
    status_code = 500
    content = ''
    try:
        response = requests.request(method, url, files=files, **kwargs)
        debug_log('Request url: %s' % response.url, debug)
        # if method == 'POST':
        #     debug_log('Request body: %s' % response.request.body, debug)
        status_code = response.status_code
        content = response.content
        if status_code >= 400:
            response.raise_for_status()
    except requests.HTTPError as err:
        raise HttpException(status_code, to_json(content), err)
    except requests.RequestException as err:
        raise ConnectionException(err)
    except (ValueError, TypeError) as err:
        raise JsonException(err)
    return response.json()


def oauth_refresh_access_token(data):
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
    return api_request(TOKEN_URL, method='POST', data=params, headers=headers)


def oauth_client_authorization(data):
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
    return api_request(TOKEN_URL, method='POST', data=params, headers=headers)


class HttpTransport(object):

    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE', 'PUT')

    def __init__(self, access_token, user_agent=None, debug=False):
        self._headers = build_headers(access_token, user_agent=user_agent)
        self._method = 'GET'
        self._files = None
        self._data = None
        self._url = None
        self._debug = debug

    def set_method(self, method):
        if method in self.SUPPORTED_METHODS:
            self._method = method
        else:
            raise AttributeError('This http method "%s" is not supported' % method)
        # here we should clean data
        return self.clean_data()

    def get(self):
        return self.set_method('GET')

    def post(self):
        return self.set_method('POST')

    def put(self):
        return self.set_method('PUT')

    def delete(self):
        return self.set_method('DELETE')

    def set_debug(self, debug):
        self._debug = debug
        return self

    def set_url(self, url, **kwargs):
        self._url = url % kwargs
        return self

    def set_data(self, data):
        self._data = data
        return self

    def clean_data(self):
        self._data = None
        return self

    def update_data(self, values):
        if self._data is None:
            self._data = {}
        self._data.update(values)
        return self

    def set_files(self, files):
        self._files = files
        return self

    def set_pagination(self, **kwargs):
        limit = kwargs.get('limit', DEFAULT_PAGINATION_LIMIT)
        offset = kwargs.get('offset', DEFAULT_PAGINATION_OFFSET)

        data = {
            'limit': limit if 0 < limit <= MAX_PAGINATION_LIMIT else DEFAULT_PAGINATION_LIMIT,
            'offset': offset if offset > 0 else DEFAULT_PAGINATION_OFFSET,
        }

        return self.update_data(data)

    def set_ordering(self, ordering):
        order_by = ordering.get('order_by', [])
        available = ordering.get('available', [])

        if not isinstance(order_by, (list, tuple, set)):
            order_by = [order_by]

        data = {
            'order_by': [item for item in order_by if item is not None and
                         (item[1:] if item[0] == '-' else item) in available]
        }

        return self.update_data(data)

    def set_filtering(self, filtering):
        filter_by = filtering.get('filter_by', {})
        available = filtering.get('available', {})

        data = {key: available[key](value) for key, value in filter_by.items() if key in available}

        return self.update_data(data)

    def request(self, **kwargs):
        if 'url' in kwargs:
            self.set_url(kwargs.pop('url'), **kwargs)
        if 'debug' in kwargs:
            self.set_debug(kwargs.pop('debug'))
        if not self._url:
            raise AttributeError(
                'Absent url parameter. Use set_url method or pass '
                'url parameter in this method.'
            )

        requests_kwargs = {
            'method': self._method,
            'headers': self._headers,
            'data': self._data,
            'debug': self._debug,
            'files': self._files,
        }
        response = HttpTransport.api_request(self._url, **requests_kwargs)
        handler = kwargs.get('handler', self._handle_response)

        return handler(response)

    @staticmethod
    def api_request(url, **kwargs):
        return api_request(url, **kwargs)

    @staticmethod
    def _handle_response(response):
        return response

    def __call__(self, **kwargs):
        return self.request(**kwargs)

# coding: utf-8
from __future__ import unicode_literals

import unittest
from datetime import datetime

import responses

from pyadmitad.transport import oauth_client_authorization, get_credentials, build_headers, \
    prepare_request_data, api_request, oauth_refresh_access_token, HttpTransport
from pyadmitad.constants import DEFAULT_REQUEST_TIMEOUT, DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET, \
    BASE_URL, TOKEN_URL
from pyadmitad.exceptions import HttpException
from pyadmitad.tests.base import BaseTestCase


class BaseTransportTestCase(BaseTestCase):

    def test_get_credentials(self):
        self.assertEqual(get_credentials('foobarbaz', '123456789'), 'Zm9vYmFyYmF6OjEyMzQ1Njc4OQ==')

    def test_build_headers(self):
        self.assertDictEqual(build_headers('foobarbaz', user_agent='test_bot'), {
            'Authorization': 'Bearer foobarbaz',
            'Connection': 'Keep-Alive',
            'User-Agent': 'test_bot',
        })

    def test_prepare_request_data(self):
        data = prepare_request_data({'foo': 42}, None, 'GET', timeout=10)

        self.assertDictEqual(data, {
            'headers': {},
            'timeout': 10,
            'verify': False,
            'allow_redirects': True,
            'params': {'foo': 42}
        })

        data = prepare_request_data({'foo': 42}, None, 'POST')

        self.assertDictEqual(data, {
            'headers': {},
            'timeout': DEFAULT_REQUEST_TIMEOUT,
            'verify': False,
            'allow_redirects': True,
            'data': {'foo': 42}
        })

        data = prepare_request_data({'foo': [None, None, 11]}, None, 'GET')

        self.assertDictEqual(data, {
            'headers': {},
            'timeout': DEFAULT_REQUEST_TIMEOUT,
            'verify': False,
            'allow_redirects': True,
            'params': {'foo': [11]}
        })

    def test_api_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                'http://example.com/',
                json={
                    'status': 'ok'
                },
                status=200
            )

            result = api_request('http://example.com/')

        self.assertIn('status', result)
        self.assertEqual('ok', result['status'])

    def test_api_request_404(self):
        with self.assertRaises(HttpException):
            with responses.RequestsMock() as resp:
                resp.add(
                    resp.GET,
                    'http://example.com/',
                    json={},
                    status=400
                )

                api_request('http://example.com/')

    def test_api_request_get(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                'http://example.com/?bar=1&baz=0',
                match_querystring=True,
                json={
                    'success': 'ok'
                },
                status=200
            )

            result = api_request('http://example.com/', data={
                'foo': [None],
                'bar': 1,
                'baz': 0
            })

        self.assertIn('success', result)

    def test_oauth_refresh_access_token(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                TOKEN_URL,
                json={
                    'access_token': 'access_token',
                    'expires_in': '604800',
                    'refresh_token': 'refresh',
                    'token_type': 'bearer',
                    'username': 'username',
                    'first_name': 'first_name',
                    'last_name': 'second_name',
                    'language': 'en',
                },
                status=200
            )

            result = oauth_refresh_access_token({
                'client_id': 'client_id',
                'client_secret': 'secret',
                'refresh_token': 'r_token',
            })

        self.assertIn('access_token', result)
        self.assertIn('expires_in', result)
        self.assertIn('refresh_token', result)
        self.assertIn('username', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)
        self.assertIn('language', result)

    def test_oauth_client_authorization(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                TOKEN_URL,
                json={
                    'access_token': 'access_token',
                    'expires_in': '604800',
                    'refresh_token': 'refresh',
                    'token_type': 'bearer',
                    'username': 'username',
                    'first_name': 'first_name',
                    'last_name': 'second_name',
                    'language': 'en',
                    'scope': 'pricate_data',
                },
                status=200
            )

            result = oauth_client_authorization({
                'client_id': 'client_id',
                'client_secret': 'secret',
                'scopes': 'private_data',
            })

        self.assertIn('access_token', result)
        self.assertIn('expires_in', result)
        self.assertIn('refresh_token', result)
        self.assertIn('username', result)
        self.assertIn('first_name', result)
        self.assertIn('last_name', result)
        self.assertIn('language', result)


class TransportTestCase(BaseTestCase):

    def test_set_default_pagination(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BASE_URL, params={
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={
                    'status': 'ok'
                },
                status=200
            )

            result = HttpTransport('access_token').get() \
                .set_pagination() \
                .request(url=BASE_URL)

        self.assertIn('status', result)

    def test_set_pagination(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BASE_URL, params={
                    'limit': 120,
                    'offset': 100
                }),
                match_querystring=True,
                json={
                    'status': 'ok'
                },
                status=200
            )

            result = HttpTransport('access_token').get() \
                .set_pagination(limit=120, offset=100) \
                .request(url=BASE_URL)

        self.assertIn('status', result)

    def test_set_ordering(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BASE_URL, params={
                    'order_by': 'name'
                }),
                match_querystring=True,
                json={
                    'status': 'ok'
                },
                status=200
            )

            result = HttpTransport('access_token').get() \
                .set_ordering(ordering={
                    'order_by': 'name',
                    'available': ['name']
                }) \
                .request(url=BASE_URL)

        self.assertIn('status', result)

    def test_set_multiple_ordering(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BASE_URL, params={
                    'order_by': ['name', '-date_updated']
                }),
                match_querystring=True,
                json={
                    'status': 'ok'
                },
                status=200
            )

            result = HttpTransport('access_token').get() \
                .set_ordering(ordering={
                    'order_by': [None, 'name', '-date_updated'],
                    'available': ['name', 'date_updated']
                }) \
                .request(url=BASE_URL)

        self.assertIn('status', result)

    def test_set_filtering(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BASE_URL, params={
                    'name': 'FOOBARBAZ',
                    'foo': 42,
                    'date_start': '01.01.2020',
                }),
                match_querystring=True,
                json={
                    'status': 'ok'
                },
                status=200
            )

            result = HttpTransport('access_token').get() \
                .set_filtering(filtering={
                    'filter_by': {
                        'name': 'foobarbaz',
                        'foo': 42,
                        'date_start': datetime(2020, 1, 1),
                        'some': 12,
                    },
                    'available': {
                        'name': lambda x: x.upper(),
                        'foo': lambda x: x,
                        'date_start': lambda x: x.strftime('%d.%m.%Y'),
                    }
                }) \
                .request(url=BASE_URL)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

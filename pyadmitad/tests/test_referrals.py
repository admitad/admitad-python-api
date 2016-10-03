# coding: utf-8
from __future__ import unicode_literals

import unittest
from datetime import datetime

import responses

from pyadmitad.items import Referrals
from pyadmitad.constants import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET
from pyadmitad.tests.base import BaseTestCase


class ReferralsTestCase(BaseTestCase):

    def test_get_referrals_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Referrals.URL, params={
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 2,
                        'limit': 20,
                        'offset': 0
                    },
                    'results': [{
                        'id': 8,
                        'payment': None,
                        'username': 'username1'
                    }, {
                        'id': 10,
                        'payment': None,
                        'username': 'username2'
                    }]
                },
                status=200
            )

            result = self.client.Referrals.get()

        self.assertIn('results', result)
        self.assertIn('_meta', result)
        self.assertIsInstance(result['results'], list)
        self.assertIsInstance(result['_meta'], dict)
        self.assertEqual(result['_meta']['limit'], 20)

    def test_get_referrals_with_filters_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Referrals.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.01.2020',
                    'limit': 40,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 2,
                        'limit': 40,
                        'offset': 0
                    },
                    'results': [{
                        'id': 8,
                        'payment': None,
                        'username': 'username1'
                    }, {
                        'id': 10,
                        'payment': None,
                        'username': 'username2'
                    }]
                },
                status=200
            )

            result = self.client.Referrals.get(date_start=datetime(2010, 1, 1), date_end=datetime(2020, 1, 1), limit=40)

        self.assertIn('results', result)
        self.assertIn('_meta', result)
        self.assertIsInstance(result['results'], list)
        self.assertIsInstance(result['_meta'], dict)
        self.assertEqual(result['_meta']['limit'], 40)

    def test_get_referrals_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Referrals.SINGLE_URL, referral_id=8),
                match_querystring=True,
                json={
                    'id': 8,
                    'payment': None,
                    'username': 'username1'
                },
                status=200
            )

            result = self.client.Referrals.getOne(8)

        self.assertEqual(result['id'], 8)


if __name__ == '__main__':
    unittest.main()

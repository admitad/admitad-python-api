# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Arecords
from pyadmitad.tests.base import BaseTestCase


class ArecordsTestCase(BaseTestCase):

    def test_get_arecords_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Arecords.URL, params={
                    'limit': 20,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    'results': [{
                        'domain': 'somewebsite.ru',
                        'website_id': 12,
                        'name': 'Some website'
                    }, {
                        'domain': 'mywebsite.kz',
                        'website_id': 10,
                        'name': 'My website'
                    }],
                    '_meta': {
                        'limit': 20,
                        'offset': 0,
                        'count': 2,
                    }
                },
                status=200
            )

            result = self.client.Arecords.get()

        self.assertEqual(len(result['results']), 2)

    def test_get_single_arecords_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Arecords.FOR_WEBSITE_URL, website_id=10),
                match_querystring=True,
                json={
                    'results': [{
                        'domain': 'mywebsite.kz',
                        'website_id': 10,
                        'name': 'My website'
                    }],
                    '_meta': {
                        'limit': 20,
                        'offset': 0,
                        'count': 1,
                    }
                },
                status=200
            )

            result = self.client.Arecords.getForWebsite(10)

        self.assertEqual(len(result['results']), 1)


if __name__ == '__main__':
    unittest.main()

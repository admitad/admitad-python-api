# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import BrokenLinks, ManageBrokenLinks
from pyadmitad.tests.base import BaseTestCase


class BrokenLinksTestCase(BaseTestCase):

    def test_get_broken_links_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BrokenLinks.URL, params={
                    'limit': 50,
                    'offset': 2,
                    'website': [1, 2, 3],
                    'campaign': [1, 2],
                    'search': 'some',
                    'reason': 0,
                    'date_start': '01.01.2010',
                    'date_end': '01.01.2020'
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.BrokenLinks.get(
                website=[1, 2, 3], campaign=[1, 2],
                search='some', reason=0,
                date_start='01.01.2010', date_end='01.01.2020',
                limit=50, offset=2
            )

        self.assertIn('status', result)

    def test_get_single_broken_link_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BrokenLinks.SINGLE_URL, broken_link_id=10),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.BrokenLinks.getOne(10)

        self.assertIn('status', result)


class ManageBrokenLinksTestCase(BaseTestCase):

    def test_resolve_broken_link_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(ManageBrokenLinks.RESOLVE_URL),
                json={'status': 'ok'},
                status=200
            )

            result = self.client.ManageBrokenLinks.resolve([10, 20])

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

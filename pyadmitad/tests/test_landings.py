# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Landings, LandingsForWebsite
from pyadmitad.tests.base import BaseTestCase


class LandingsTestCase(BaseTestCase):

    def test_landings_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Landings.URL, campaign_id=8, params={
                    'limit': 2,
                    'offset': 0
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Landings.get(8, limit=2, offset=0)

        self.assertIn('status', result)


class LandingsForWebsiteTestCase(BaseTestCase):

    def test_landings_for_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(LandingsForWebsite.URL, campaign_id=8, website_id=11, params={
                    'limit': 1,
                    'offset': 0
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.LandingsForWebsite.get(8, 11, limit=1)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

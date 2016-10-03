# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Banners, BannersForWebsite
from pyadmitad.tests.base import BaseTestCase


class BannersTestCase(BaseTestCase):

    def test_get_banners_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Banners.URL, campaign_id=12, params={
                    'limit': 40,
                    'offset': 10,
                    'mobile_content': 'true'
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Banners.get(12, mobile_content=True, limit=40, offset=10)

        self.assertIn('status', result)


class BannersForWebsiteTestCase(BaseTestCase):

    def test_get_banners_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(BannersForWebsite.URL, campaign_id=12, website_id=10, params={
                    'limit': 40,
                    'offset': 10,
                    'mobile_content': 'true',
                    'landing': 6,
                    'uri_scheme': 'https'
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.BannersForWebsite.get(12, 10, mobile_content=True,
                                                       landing=6, uri_scheme='https',
                                                       limit=40, offset=10)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

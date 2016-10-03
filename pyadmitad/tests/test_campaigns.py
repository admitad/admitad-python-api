# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Campaigns, CampaignsForWebsite, \
    CampaignsManage
from pyadmitad.tests.base import BaseTestCase


class CampaignsTestCase(BaseTestCase):

    def test_get_campaigns_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Campaigns.URL, params={
                    'website': 10,
                    'has_tool': ['deeplink', 'retag'],
                    'limit': 10,
                    'offset': 0,
                    'language': 'en'
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Campaigns.get(website=10, has_tool=['deeplink', 'retag'],
                                               limit=10, offset=0, language='en')

        self.assertIn('status', result)

    def test_get_campaigns_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Campaigns.SINGLE_URL, campaign_id=10),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Campaigns.getOne(10)

        self.assertIn('status', result)


class CampaignsForWebsiteTestCase(BaseTestCase):

    def test_get_campaigns_for_websites_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignsForWebsite.URL, website_id=16, params={
                    'limit': 26,
                    'offset': 10
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CampaignsForWebsite.get(16, limit=26, offset=10)

        self.assertIn('status', result)

    def test_get_campaigns_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignsForWebsite.SINGLE_URL, website_id=10, campaign_id=88),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CampaignsForWebsite.getOne(10, 88)

        self.assertIn('status', result)


class CampaignsConnectWebsiteTestCase(BaseTestCase):

    def test_campaign_connect_websites_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(CampaignsManage.CONNECT_URL, campaign_id=10, website_id=22),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CampaignsManage.connect(10, 22)

        self.assertIn('status', result)

    def test_campaign_disconnect_websites_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(CampaignsManage.DISCONNECT_URL, campaign_id=10, website_id=22),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CampaignsManage.disconnect(10, 22)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

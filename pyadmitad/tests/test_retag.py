# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Retag, RetagManager
from pyadmitad.constants import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET
from pyadmitad.tests.base import BaseTestCase


class RetagTestCase(BaseTestCase):

    def test_retag_get_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Retag.URL, params={
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET,
                    'website': 10,
                    'active': 1
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Retag.get(website=10, active=True)

        self.assertIn('status', result)

    def test_retag_get_single_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Retag.SINGLE_URL, retag_id=11),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Retag.getOne(11)

        self.assertIn('status', result)

    def test_retag_get_levels_for_campaign_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Retag.LEVELS_FOR_CAMPAIGN_URL, campaign_id=20),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Retag.getLevelsForCampaign(20)

        self.assertIn('status', result)

    def test_retag_get_levels_for_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Retag.LEVELS_FOR_WEBSITE_URL, website_id=78),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Retag.getLevelsForWebsite(78)

        self.assertIn('status', result)


class ManageRetagTestCase(BaseTestCase):

    def test_retag_create(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(RetagManager.CREATE_URL),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.RetagManager.create(
                website=10,
                level=2,
                active=False,
                script='print',
                comment='some comment'
            )

        self.assertIn('status', result)

    def test_retag_update(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(RetagManager.UPDATE_URL, retag_id=50),
                json={'status': 'ok'},
                status=200
            )

            result = self.client.RetagManager.update(
                50,
                level=4,
                active=True
            )

        self.assertIn('status', result)

    def test_retag_delete(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(RetagManager.DELETE_URL, retag_id=50),
                json={'status': 'ok'},
                status=200
            )

            result = self.client.RetagManager.delete(50)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

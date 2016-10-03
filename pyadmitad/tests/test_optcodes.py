# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import OptCodes, OfferStatusOptCodesManager, ActionOptCodesManager
from pyadmitad.tests.base import BaseTestCase


class OptCodeTestCase(BaseTestCase):

    def test_get_opt_codes_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(OptCodes.URL, params={
                    'campaign': 10,
                    'website': 20,
                    'limit': 1,
                    'offset': 0,
                    'order_by': ['method']
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.OptCodes.get(
                campaign=10,
                website=20,
                limit=1,
                offset=0,
                order_by=['method']
            )

        self.assertIn('status', result)

    def test_get_opt_code_by_id_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(OptCodes.SINGLE_URL, optcode_id=12),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.OptCodes.getOne(12)

        self.assertIn('status', result)


class OffserStatusOptCodesManagerTestCase(BaseTestCase):

    def test_create_opt_code(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(OfferStatusOptCodesManager.CREATE_URL),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.OfferStatusOptCodesManager.create(
                website=10,
                campaign=20,
                desc_mode=1,
                url='https://google.com',
                method=1
            )

        self.assertIn('status', result)

    def test_update_opt_code(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(OfferStatusOptCodesManager.UPDATE_URL, optcode_id=2),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.OfferStatusOptCodesManager.update(
                2,
                desc_mode=2,
                url='https://google.com/',
                method=2
            )

        self.assertIn('status', result)


class ActionOptCodesManagerTestCase(BaseTestCase):

    def test_create_opt_code(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(ActionOptCodesManager.CREATE_URL),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.ActionOptCodesManager.create(
                website=10,
                campaign=20,
                desc_mode=1,
                url='https://google.com',
                method=1,
                action_type=1,
                status=1
            )

        self.assertIn('status', result)

    def test_update_opt_code(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(ActionOptCodesManager.UPDATE_URL, optcode_id=77),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.ActionOptCodesManager.update(
                77,
                desc_mode=2,
                url='https://google.com/',
                method=2,
                action_type=2,
                status=1
            )

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

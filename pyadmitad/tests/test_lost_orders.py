# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import LostOrders, LostOrdersManager
from pyadmitad.tests.base import BaseTestCase


class LostOrdersTestCase(BaseTestCase):

    def test_get_lost_orders_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(LostOrders.URL, params={
                    'limit': 20,
                    'offset': 1
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.LostOrders.get(
                limit=20,
                offset=1
            )

        self.assertIn('status', result)

    def test_get_lost_order_by_id_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(LostOrders.SINGLE_URL, lost_order_id=12),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.LostOrders.getOne(12)

        self.assertIn('status', result)


class LostOrdersManagerTestCase(BaseTestCase):

    def test_create_lost_order(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(LostOrdersManager.CREATE_URL),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.LostOrdersManager.create(
                attachments=['./pyadmitad/tests/data/image.png'],
                website=10,
                advcampaign=20,
                order_id='asd3f3',
                order_date='01.01.2010',
                order_price=1200,
                comment='foo bar baz'
            )

        self.assertIn('status', result)

    def test_delete_lost_order(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.DELETE,
                self.prepare_url(LostOrdersManager.DELETE_URL, lost_order_id=2),
                match_querystring=True,
                json={'status': 'ok'},
                status=200,
            )
            result = self.client.LostOrdersManager.delete(2)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

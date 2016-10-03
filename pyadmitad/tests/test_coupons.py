# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Coupons, CouponsForWebsite, CouponsCategories
from pyadmitad.tests.base import BaseTestCase


class CouponsTestCase(BaseTestCase):

    def test_get_coupons_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Coupons.URL, params={
                    'campaign': [1, 5, 6],
                    'campaign_category': [11, 12],
                    'category': [22, 23],
                    'type': 'some',
                    'limit': 10,
                    'offset': 0,
                    'order_by': ['name', '-rating']
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Coupons.get(
                campaign=[1, 5, 6], campaign_category=[11, 12],
                category=[22, 23], type='some', limit=10, offset=0,
                order_by=['name', '-rating'])

        self.assertIn('status', result)

    def test_get_coupons_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Coupons.SINGLE_URL, coupon_id=42),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Coupons.getOne(42)

        self.assertIn('status', result)


class CouponsForWebsiteTestCase(BaseTestCase):

    def test_get_coupons_for_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CouponsForWebsite.URL, website_id=1, params={
                    'campaign': [1, 5, 6],
                    'campaign_category': [11, 12],
                    'category': [22, 23],
                    'type': 'some',
                    'limit': 10,
                    'offset': 0,
                    'order_by': ['name', '-rating']
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CouponsForWebsite.get(
                1, campaign=[1, 5, 6], campaign_category=[11, 12],
                category=[22, 23], type='some', limit=10, offset=0,
                order_by=['name', '-rating'])

        self.assertIn('status', result)

    def test_get_coupons_for_website_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CouponsForWebsite.SINGLE_URL, website_id=10, campaign_id=20),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CouponsForWebsite.getOne(10, 20)

        self.assertIn('status', result)


class CouponsCategoriesTestCase(BaseTestCase):

    def test_get_categories_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CouponsCategories.URL, params={
                    'limit': 10,
                    'offset': 0
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CouponsCategories.get(limit=10, offset=0)

        self.assertIn('status', result)

    def test_get_categorty_with_id_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CouponsCategories.SINGLE_URL, coupon_category_id=200),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.CouponsCategories.getOne(200)

        self.assertIn('status', result)

if __name__ == '__main__':
    unittest.main()

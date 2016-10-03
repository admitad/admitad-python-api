# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.tests.base import BaseTestCase
from pyadmitad.items.auxiliary import WebsiteTypes, WebsiteRegions, \
    SystemLanguages, SystemCurrencies, AdvertiserServices, CampaignCategories


class WebsiteTypesTestCase(BaseTestCase):

    def test_get_website_types_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(WebsiteTypes.URL, params={
                    'limit': 5,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 9,
                        'limit': 5,
                        'offset': 0
                    },
                    'results': [
                        'website',
                        'doorway',
                        'contextual',
                        'youtube',
                        'social_app',
                    ]
                },
                status=200
            )

            result = self.client.WebsiteTypes.get(limit=5)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(5, len(result['results']))


class WebsiteRegionsTestCase(BaseTestCase):

    def test_get_website_regions_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(WebsiteRegions.URL, params={
                    'limit': 2,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'limit': 2,
                        'offset': 0,
                        'count': 6
                    },
                    'results': ['RU', 'EN']
                },
                status=200
            )

            result = self.client.WebsiteRegions.get(limit=2)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(2, len(result['results']))


class SystemLanguagesTestCase(BaseTestCase):

    def test_get_languages_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(SystemLanguages.URL, params={
                    'limit': 2,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 4,
                        'limit': 2,
                        'offset': 1
                    },
                    'results': [{
                        'flag': 'http://cdn.admitad.com/images/flags/en.svg',
                        'language': 'English',
                        'language_code': 'en'
                    }, {
                        'flag': 'http://cdn.admitad.com/images/flags/de.svg',
                        'language': 'Deutsch',
                        'language_code': 'de'
                    }]
                },
                status=200
            )

            result = self.client.SystemLanguages.get(limit=2)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(2, len(result['results']))

    def test_get_language_request_with_code(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(SystemLanguages.SINGLE_URL, code='en'),
                json={
                    'flag': 'http://cdn.admitad.com/images/flags/en.svg',
                    'language': 'English',
                    'language_code': 'en'
                },
                status=200
            )

            result = self.client.SystemLanguages.getOne(code='en')

        self.assertIn('flag', result)
        self.assertIn('language', result)
        self.assertIn('language_code', result)


class SystemCurrenciesTestCase(BaseTestCase):

    def test_get_currencies_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(SystemCurrencies.URL, params={
                    'limit': 1,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 4,
                        'limit': 1,
                        'offset': 0
                    },
                    'results': [{
                        'code': 'USD',
                        'min_sum': '25.00',
                        'name': 'American dollar',
                        'sign': '$'
                    }]
                },
                status=200
            )

            result = self.client.SystemCurrencies.get(limit=1)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(1, len(result['results']))


class AdvertiserServicesTestCase(BaseTestCase):

    def test_get_advertiser_services(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(AdvertiserServices.URL, params={
                    'limit': 2,
                    'offset': 1
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 12,
                        'limit': 2,
                        'offset': 1
                    },
                    'results': [{
                        'allowed_referrers': '',
                        'id': 4,
                        'logo': 'http://cdn.admitad.com/adservice/images/f7e67e924fa05952f03e0c8c40a11651.png',
                        'name': 'Google AdWords',
                        'url': 'http://adwords.google.com/'
                    }, {
                        'allowed_referrers': 'facebook.com',
                        'id': 3,
                        'logo': 'http://cdn.admitad.com/adservice/images/e6fee9e2ca69a2113d1339ecbe361ea5.png',
                        'name': 'Facebook',
                        'url': 'http://facebook.com/'
                    }]
                },
                status=200
            )

            result = self.client.AdvertiserServices.get(limit=2, offset=1)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(2, len(result['results']))

    def test_get_advertiser_services_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(AdvertiserServices.SINGLE_URL, id=3),
                match_querystring=True,
                json={
                    'allowed_referrers': 'facebook.com',
                    'id': 3,
                    'logo': 'http://cdn.admitad.com/adservice/images/e6fee9e2ca69a2113d1339ecbe361ea5.png',
                    'name': 'Facebook',
                    'url': 'http://facebook.com/'
                },
                status=200
            )

            result = self.client.AdvertiserServices.getOne(3)

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('url', result)

    def test_get_advertiser_services_with_kind(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(AdvertiserServices.KIND_URL, kind='website', params={
                    'limit': 1,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 10,
                        'limit': 20,
                        'offset': 0
                    },
                    'results': [{
                        'allowed_referrers': 'facebook.com',
                        'id': 3,
                        'logo': 'http://cdn.admitad.com/adservice/images/e6fee9e2ca69a2113d1339ecbe361ea5.png',
                        'name': 'Facebook',
                        'url': 'http://facebook.com/'
                    }]
                },
                status=200
            )

            result = self.client.AdvertiserServices.getForKind('website', limit=1)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(1, len(result['results']))


class CampaignsCategoriesTestCase(BaseTestCase):

    def test_get_campaigns_categories(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignCategories.URL, params={
                    'limit': 2,
                    'offset': 1,
                    'order_by': 'name'
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 12,
                        'limit': 2,
                        'offset': 1
                    },
                    'results': [{
                        'id': 13,
                        'language': 'en',
                        'name': 'MobileCategory',
                        'parent': None
                    }, {
                        'id': 33,
                        'language': 'en',
                        'name': 'ZooCategory',
                        'parent': None
                    }]
                },
                status=200
            )

            result = self.client.CampaignCategories.get(limit=2, offset=1, order_by='name')

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(2, len(result['results']))

    def test_get_campaigns_categories_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(CampaignCategories.SINGLE_URL, id='13'),
                match_querystring=True,
                json={
                    'id': 13,
                    'language': 'en',
                    'name': 'MobileCategory',
                    'parent': None
                },
                status=200
            )

            result = self.client.CampaignCategories.getOne(13)

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('parent', result)
        self.assertIn('language', result)


if __name__ == '__main__':
    unittest.main()

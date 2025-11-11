# coding: utf-8
from __future__ import unicode_literals

import unittest
from urllib.parse import quote

import responses

from admitad.items import Websites, WebsitesManage, WebsitesManageV2
from admitad.tests.base import BaseTestCase


class WebsitesTestCase(BaseTestCase):

    def test_get_websites_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Websites.URL, params={
                    'limit': 1,
                    'offset': 2
                }),
                match_querystring=True,
                json={
                    'results': [{
                        'id': 4,
                        'status': 'active',
                        'kind': 'website',
                        'name': 'FooName',
                        'categories': [1, 2],
                        'adservice': None,
                        'creation_date': '2010-04-17T21:54:45',
                        'description': '',
                        'is_old': True,
                        'mailing_targeting': False,
                        'regions': ['RU'],
                        'site_url': 'https://foo.bar/',
                        'validation_passed': False,
                        'verification_code': '11c0sd4d14',
                        'atnd_hits': 122,
                        'atnd_visits': 10,
                    }],
                    '_meta': {
                        'limit': 1,
                        'offset': 2,
                        'count': 9,
                    }
                },
                status=200
            )

            result = self.client.Websites.get(limit=1, offset=2)

        self.assertEqual(len(result['results']), 1)
        self.assertIn('count', result['_meta'])
        for item in result['results']:
            self.assertIn('id', item)
            self.assertIn('kind', item)
            self.assertIn('status', item)
            self.assertIn('name', item)
            self.assertIn('categories', item)
            self.assertIn('adservice', item)
            self.assertIn('creation_date', item)
            self.assertIn('description', item)
            self.assertIn('is_old', item)
            self.assertIn('mailing_targeting', item)
            self.assertIn('regions', item)
            self.assertIn('site_url', item)
            self.assertIn('validation_passed', item)
            self.assertIn('verification_code', item)
            self.assertIn('atnd_hits', item)
            self.assertIn('atnd_visits', item)

    def test_get_websites_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Websites.SINGLE_URL, website_id=4),
                json={
                    'id': 4,
                    'status': 'active',
                    'kind': 'website',
                    'name': 'FooName',
                    'categories': [{
                        'id': 1,
                        'language': 'en',
                        'name': 'Cat1',
                        'parent': None
                    }, {
                        'id': 2,
                        'language': 'en',
                        'name': 'Cat2',
                        'parent': None
                    }],
                    'adservice': None,
                    'creation_date': '2010-04-17T21:54:45',
                    'description': '',
                    'is_old': True,
                    'mailing_targeting': False,
                    'regions': ['RU'],
                    'site_url': 'https://foo.bar/',
                    'validation_passed': False,
                    'verification_code': '11c0sd4d14',
                    'atnd_hits': 122,
                    'atnd_visits': 10,
                },
                status=200
            )

            result = self.client.Websites.getOne(4)

        self.assertIn('id', result)
        self.assertIn('kind', result)
        self.assertIn('status', result)
        self.assertIn('name', result)
        self.assertIn('categories', result)
        self.assertIn('adservice', result)
        self.assertIn('creation_date', result)
        self.assertIn('description', result)
        self.assertIn('is_old', result)
        self.assertIn('mailing_targeting', result)
        self.assertIn('regions', result)
        self.assertIn('site_url', result)
        self.assertIn('validation_passed', result)
        self.assertIn('verification_code', result)
        self.assertIn('atnd_hits', result)
        self.assertIn('atnd_visits', result)


class WebsitesManageTestCase(BaseTestCase):

    def test_create_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManage.CREATE_URL),
                match_querystring=True,
                json={
                    'id': 42,
                    'status': 'new',
                    'kind': 'website',
                    'name': 'FooBar',
                    'categories': [{
                        'id': 1,
                        'language': 'en',
                        'name': 'Cat1',
                        'parent': None
                    }, {
                        'id': 2,
                        'language': 'en',
                        'name': 'Cat2',
                        'parent': None
                    }],
                    'adservice': None,
                    'creation_date': '2016-10-10T11:54:45',
                    'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
                    'is_old': False,
                    'mailing_targeting': True,
                    'regions': ['RU'],
                    'site_url': 'https://foobar.baz/',
                    'validation_passed': False,
                    'verification_code': '244a5d4a14',
                    'atnd_hits': 500,
                    'atnd_visits': 100,
                },
                status=200
            )

            result = self.client.WebsitesManage.create(
                name='FooBar',
                kind='website',
                language='en',
                site_url='https://foobar.baz/',
                description='Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
                categories=[1, 2],
                regions=['RU'],
                atnd_visits=500,
                atnd_hits=100,
                mailing_targeting=True
            )

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('status', result)
        self.assertIn('kind', result)
        self.assertIn('verification_code', result)

    def test_update_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManage.UPDATE_URL, website_id=42),
                json={
                    'id': 42,
                    'status': 'new',
                    'kind': 'website',
                    'name': 'FooBarBaz',
                    'categories': [{
                        'id': 1,
                        'language': 'en',
                        'name': 'Cat1',
                        'parent': None
                    }, {
                        'id': 2,
                        'language': 'en',
                        'name': 'Cat2',
                        'parent': None
                    }],
                    'adservice': None,
                    'creation_date': '2016-10-10T11:54:45',
                    'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
                    'is_old': False,
                    'mailing_targeting': True,
                    'regions': ['RU'],
                    'site_url': 'https://foobar.bar/',
                    'validation_passed': False,
                    'verification_code': '244a5d4a14',
                    'atnd_hits': 1000,
                    'atnd_visits': 100,
                },
                status=200
            )

            result = self.client.WebsitesManage.update(
                42,
                name='FooBarBaz',
                atnd_visits=1000,
            )

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('atnd_visits', result)

    def test_verify_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManage.VERIFY_URL, website_id=42),
                json={
                    'message': 'Message',
                    'success': 'Accepted'
                },
                status=200
            )

            result = self.client.WebsitesManage.verify(42)

        self.assertIn('message', result)
        self.assertIn('success', result)

    def test_delete_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManage.DELETE_URL, website_id=42),
                json={
                    'message': 'Message',
                    'success': 'Deleted'
                },
                status=200
            )

            result = self.client.WebsitesManage.delete(42)

        self.assertIn('message', result)
        self.assertIn('success', result)


class WebsitesManageV2TestCase(BaseTestCase):

    def test_create_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManageV2.CREATE_URL),
                match_querystring=True,
                json={
                    'id': 30,
                    'status': 'new',
                    'kind': 'social_network_vk',
                    'name': 'test website',
                    'site_url': 'http://vk.com/xui',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': '',
                    'validation_passed': False,
                    'is_lite': False,
                },
                status=200
            )

            result = self.client.WebsitesManageV2.create(
                name='test website',
                kind='social_network_vk',
                url='http://vk.com/xui',
                category=[1, 2],
                region=['RU'],
            )

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('status', result)
        self.assertIn('kind', result)
        self.assertIn('verification_code', result)
        self.assertIn('site_url', result)
        self.assertIn('creation_date', result)
        self.assertIn('is_old', result)
        self.assertIn('account_id', result)
        self.assertIn('validation_passed', result)
        self.assertIn('is_lite', result)

    def test_update_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManageV2.UPDATE_URL, website_id=30),
                json={
                    'id': 30,
                    'status': 'new',
                    'kind': 'social_network_vk',
                    'name': 'updated website',
                    'site_url': 'http://vk.com/updated',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': '',
                    'validation_passed': False,
                    'is_lite': False,
                },
                status=200
            )

            result = self.client.WebsitesManageV2.update(
                30,
                name='updated website',
                url='http://vk.com/updated',
            )

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('site_url', result)
        self.assertEqual(result['name'], 'updated website')
        self.assertEqual(result['site_url'], 'http://vk.com/updated')

    def test_verify_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManageV2.VERIFY_URL, website_id=30),
                json={
                    'success': 'Accepted',
                    'message': 'Площадка прошла автоматическую проверку.'
                },
                status=202
            )

            result = self.client.WebsitesManageV2.verify(30)

        self.assertIn('success', result)
        self.assertIn('message', result)
        self.assertEqual(result['success'], 'Accepted')

    def test_delete_website_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(WebsitesManageV2.DELETE_URL, website_id=30),
                json={},
                status=200
            )

            result = self.client.WebsitesManageV2.delete(30)

        self.assertEqual(result, {})

    def test_get_websites_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(WebsitesManageV2.GET_URL, params={
                    'limit': 10,
                    'offset': 0
                }),
                match_querystring=True,
                json={
                    'results': [{
                        'id': 30,
                        'status': 'new',
                        'kind': 'social_network_vk',
                        'name': 'test website',
                        'site_url': 'http://vk.com/xui',
                        'verification_code': '074a583c47',
                        'creation_date': '2025-08-28T12:54:24',
                        'is_old': False,
                        'account_id': '',
                        'validation_passed': False,
                        'is_lite': False,
                    }],
                    '_meta': {
                        'limit': 10,
                        'offset': 0,
                        'count': 1,
                    }
                },
                status=200
            )

            result = self.client.WebsitesManageV2.get(limit=10, offset=0)

        self.assertIn('results', result)
        self.assertIn('_meta', result)
        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['_meta']['count'], 1)

    def test_get_website_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(WebsitesManageV2.GET_ONE_URL, website_id=30),
                json={
                    'id': 30,
                    'status': 'new',
                    'kind': 'social_network_vk',
                    'name': 'test website',
                    'site_url': 'http://vk.com/xui',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': '',
                    'validation_passed': False,
                    'is_lite': False,
                },
                status=200
            )

            result = self.client.WebsitesManageV2.getOne(30)

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('status', result)
        self.assertIn('kind', result)
        self.assertIn('verification_code', result)
        self.assertIn('site_url', result)
        self.assertIn('creation_date', result)
        self.assertIn('is_old', result)
        self.assertIn('account_id', result)
        self.assertIn('validation_passed', result)
        self.assertIn('is_lite', result)

    def test_get_website_request_with_name(self):
        with responses.RequestsMock() as resp:
            encoded_name = quote('Google Ads', safe='')
            resp.add(
                resp.GET,
                self.prepare_url(WebsitesManageV2.GET_ONE_URL, website_id=encoded_name, params={
                    'search_by': 'name'
                }),
                match_querystring=True,
                json={
                    'id': 42,
                    'status': 'active',
                    'kind': 'social_network_google_ads',
                    'name': 'Google Ads',
                    'site_url': 'https://ads.google.com/profile',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': 'google_ads_123',
                    'validation_passed': True,
                    'is_lite': False,
                },
                status=200
            )

            result = self.client.WebsitesManageV2.getOne('Google Ads', search_by='name')

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('status', result)
        self.assertIn('kind', result)
        self.assertEqual(result['name'], 'Google Ads')
        self.assertEqual(result['kind'], 'social_network_google_ads')
        self.assertEqual(result['account_id'], 'google_ads_123')

    def test_get_website_request_with_name_default_search_by_id(self):
        """Test that default search_by is 'id' when not specified"""
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(WebsitesManageV2.GET_ONE_URL, website_id=30),
                json={
                    'id': 30,
                    'status': 'new',
                    'kind': 'social_network_vk',
                    'name': 'test website',
                    'site_url': 'http://vk.com/xui',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': '',
                    'validation_passed': False,
                    'is_lite': False,
                },
                status=200
            )

            # Test without search_by parameter (should default to 'id')
            result = self.client.WebsitesManageV2.getOne(30)

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertEqual(result['id'], 30)
        self.assertEqual(result['name'], 'test website')

    def test_get_website_request_with_string_id_and_search_by_id(self):
        """Test that string ID works when search_by='id'"""
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(WebsitesManageV2.GET_ONE_URL, website_id=123),
                json={
                    'id': 123,
                    'status': 'active',
                    'kind': 'website',
                    'name': 'My Website',
                    'site_url': 'https://example.com',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': '',
                    'validation_passed': True,
                    'is_lite': False,
                },
                status=200
            )

            # Test with string ID and explicit search_by='id'
            result = self.client.WebsitesManageV2.getOne('123', search_by='id')

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertEqual(result['id'], 123)
        self.assertEqual(result['name'], 'My Website')

    def test_get_website_request_with_special_characters_in_name(self):
        """Test that names with special characters work correctly"""
        with responses.RequestsMock() as resp:
            # URL-encode the name to match what the library will send
            encoded_name = quote('Test-Website_123', safe='')
            resp.add(
                resp.GET,
                self.prepare_url(WebsitesManageV2.GET_ONE_URL, website_id=encoded_name, params={
                    'search_by': 'name'
                }),
                match_querystring=True,
                json={
                    'id': 99,
                    'status': 'active',
                    'kind': 'website',
                    'name': 'Test-Website_123',
                    'site_url': 'https://test-website-123.com',
                    'verification_code': '074a583c47',
                    'creation_date': '2025-08-28T12:54:24',
                    'is_old': False,
                    'account_id': '',
                    'validation_passed': True,
                    'is_lite': False,
                },
                status=200
            )

            result = self.client.WebsitesManageV2.getOne('Test-Website_123', search_by='name')

        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertEqual(result['name'], 'Test-Website_123')
        self.assertEqual(result['id'], 99)


if __name__ == '__main__':
    unittest.main()

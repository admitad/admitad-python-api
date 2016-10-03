# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Websites, WebsitesManage
from pyadmitad.tests.base import BaseTestCase


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
                    'site_url': 'https://foobar.bar/',
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


if __name__ == '__main__':
    unittest.main()

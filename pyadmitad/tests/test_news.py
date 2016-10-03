# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import News
from pyadmitad.tests.base import BaseTestCase


class AnnouncementsTestCase(BaseTestCase):

    def test_get_announcements_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(News.URL, params={
                    'limit': 2,
                    'offset': 2
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 50,
                        'limit': 2,
                        'offset': 2
                    },
                    'results': [{
                        'id': 12,
                        'url': '',
                        'language': 'en',
                        'content': '<p>full text</p>',
                        'short_content': 'short text',
                        'advcampaign': {
                            'id': 18,
                            'name': 'AdvCamp'
                        },
                        'datetime': '2009-12-02T23:08:45'
                    }, {
                        'id': 16,
                        'url': '',
                        'language': 'en',
                        'content': '<p>full text 2</p>',
                        'short_content': 'short text 2',
                        'advcampaign': {
                            'id': 18,
                            'name': 'AdvCamp'
                        },
                        'datetime': '2009-12-02T23:09:00'
                    }]
                },
                status=200
            )

            result = self.client.News.get(limit=2, offset=2)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(2, len(result['results']))

    def test_get_announcements_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(News.SINGLE_URL, news_id=12),
                match_querystring=True,
                json={
                    'id': 12,
                    'url': '',
                    'language': 'en',
                    'content': '<p>full text</p>',
                    'short_content': 'short text',
                    'advcampaign': {
                        'id': 18,
                        'name': 'AdvCamp'
                    },
                    'datetime': '2009-12-02T23:08:45'
                },
                status=200
            )

            result = self.client.News.getOne(12)

        self.assertIn('id', result)
        self.assertIn('url', result)
        self.assertIn('content', result)
        self.assertIn('datetime', result)


if __name__ == '__main__':
    unittest.main()

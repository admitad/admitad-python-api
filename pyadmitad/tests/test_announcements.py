# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Announcements
from pyadmitad.tests.base import BaseTestCase


class AnnouncementsTestCase(BaseTestCase):

    def test_get_announcements_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Announcements.URL, params={
                    'limit': 1,
                    'offset': 230
                }),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 50,
                        'limit': 1,
                        'offset': 230
                    },
                    'results': [{
                        'message': 'Message',
                        'id': 264,
                        'advcampaign': {
                            'id': 8,
                            'name': 'AdvCamp'
                        },
                        'event': 'request_accepted'
                    }]
                },
                status=200
            )

            result = self.client.Announcements.get(limit=1, offset=230)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(1, len(result['results']))

    def test_get_announcements_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Announcements.SINGLE_URL, announcement_id=264),
                match_querystring=True,
                json={
                    '_meta': {
                        'count': 50,
                        'limit': 1,
                        'offset': 230
                    },
                    'results': [{
                        'message': 'Message',
                        'id': 264,
                        'advcampaign': {
                            'id': 8,
                            'name': 'AdvCamp'
                        },
                        'event': 'request_accepted'
                    }]
                },
                status=200
            )

            result = self.client.Announcements.getOne(264)

        self.assertIn('_meta', result)
        self.assertIn('results', result)
        self.assertEqual(1, len(result['results']))


if __name__ == '__main__':
    unittest.main()

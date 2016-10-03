# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.tests.base import BaseTestCase
from pyadmitad.items import DeeplinksManage


class DeeplinksManageTestCase(BaseTestCase):

    def test_deeplinks_create_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(DeeplinksManage.CREATE_URL, website_id=9, campaign_id=10, params={
                    'subid': '0987654321234567890',
                    'ulp': 'https://google.com/'
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.DeeplinksManage.create(9, 10, subid='0987654321234567890', ulp='https://google.com/')

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

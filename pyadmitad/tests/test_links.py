# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import LinksValidator
from pyadmitad.tests.base import BaseTestCase


class LinksValidationTestCase(BaseTestCase):

    def test_link_validation_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(LinksValidator.URL, params={
                    'link': 'https://google.com/'
                }),
                match_querystring=True,
                json={
                    'message': 'Link tested.',
                    'success': 'Accepted'
                },
                status=200
            )

            result = self.client.LinksValidator.get('https://google.com/')

        self.assertIn('message', result)
        self.assertIn('success', result)


if __name__ == '__main__':
    unittest.main()

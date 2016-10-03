# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Tickets, TicketsManager
from pyadmitad.constants import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET
from pyadmitad.tests.base import BaseTestCase


class TicketsTestCase(BaseTestCase):

    def test_get_tickets_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Tickets.URL, params={
                    'status': 1,
                    'date_start': '01.01.2010',
                    'date_end': '01.01.2020',
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Tickets.get(
                status=1,
                date_start='01.01.2010',
                date_end='01.01.2020'
            )

        self.assertIn('status', result)

    def test_get_single_ticket_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Tickets.SINGLE_URL, ticket_id=22),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )

            result = self.client.Tickets.getOne(22)

        self.assertIn('status', result)


class ManageTicketsTestCase(BaseTestCase):

    def test_create(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(TicketsManager.CREATE_URL),
                json={'status': 'ok'},
                status=200
            )

            result = self.client.TicketsManager.create(
                subject='foo',
                text='bar',
                campaign=90,
                category=20,
                priority=2,
            )

        self.assertIn('status', result)

    def test_commenting(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(TicketsManager.COMMENT_URL, ticket_id=276),
                json={'status': 'ok'},
                status=200
            )

            result = self.client.TicketsManager.comment(276, text='comment text')

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Payments, PaymentsStatement, PaymentsManage
from pyadmitad.constants import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET
from pyadmitad.tests.base import BaseTestCase


class PaymentsTestCase(BaseTestCase):

    def test_get_payments_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Payments.URL, params={
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Payments.get()

        self.assertIn('status', result)

    def test_get_payments_request_with_id(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Payments.SINGLE_URL, payment_id=167),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.Payments.getOne(167)

        self.assertIn('status', result)


class PaymentsStatementTestCase(BaseTestCase):

    def test_get_payments_statement_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(PaymentsStatement.URL, payment_id=12, params={
                    'detailed': 1,
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.PaymentsStatement.get(12, detailed=True)

        self.assertIn('status', result)


class PaymentsManageTestCase(BaseTestCase):

    def test_create_payments_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(PaymentsManage.CREATE_URL, code='USD'),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.PaymentsManage.create('USD')

        self.assertIn('status', result)

    def test_confirm_payments_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(PaymentsManage.CONFIRM_URL, payment_id=98),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.PaymentsManage.confirm(98)

        self.assertIn('status', result)

    def test_delete_payments_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                self.prepare_url(PaymentsManage.DELETE_URL, payment_id=98),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.PaymentsManage.delete(98)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

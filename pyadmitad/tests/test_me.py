# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import Me, Balance, PaymentsSettings
from pyadmitad.tests.base import BaseTestCase


class MeTestCase(BaseTestCase):

    def test_me_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Me.URL),
                json={
                    'id': 1,
                    'username': 'username',
                    'first_name': 'first_name',
                    'last_name': 'last_name',
                    'language': 'ru'
                },
                status=200
            )

            result = self.client.Me.get()

        self.assertEqual(result['id'], 1)
        self.assertEqual(result['username'], 'username')
        self.assertEqual(result['first_name'], 'first_name')
        self.assertEqual(result['last_name'], 'last_name')
        self.assertEqual(result['language'], 'ru')


class BalanceTestCase(BaseTestCase):

    def test_balance_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Balance.URL),
                json=[{
                    'currency': 'USD',
                    'balance': '20000.00'
                }, {
                    'currency': 'EUR',
                    'balance': '0.00'
                }],
                status=200
            )

            result = self.client.Balance.get()

        self.assertEqual(len(result), 2)
        for item in result:
            self.assertIn('balance', item)
            self.assertIn('currency', item)

    def test_balance_extended_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(Balance.EXTENDED_URL),
                json=[{
                    'currency': 'USD',
                    'balance': '20000.00',
                    'processing': '20.00',
                    'today': '0.00',
                    'stalled': '100.00'
                }, {
                    'currency': 'EUR',
                    'balance': '0.00',
                    'processing': '2100.00',
                    'today': '0.00',
                    'stalled': '0.00'
                }],
                status=200
            )

            result = self.client.Balance.get(extended=True)

        self.assertEqual(len(result), 2)
        for item in result:
            self.assertIn('balance', item)
            self.assertIn('currency', item)
            self.assertIn('processing', item)
            self.assertIn('today', item)
            self.assertIn('stalled', item)


class PaymentsSettingsTestCase(BaseTestCase):

    def test_payments_settings_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(PaymentsSettings.URL),
                json=[{
                    'id': 11,
                    'name': 'some_name',
                    'currency': ['USD'],
                    'withdrawal_type': 'webmoney'
                }, {
                    'id': 18,
                    'name': 'some_another',
                    'currency': ['EUR'],
                    'withdrawal_type': 'paypal'
                }],
                status=200
            )

            result = self.client.PaymentsSettings.get()

        self.assertEqual(len(result), 2)
        for item in result:
            self.assertIn('id', item)
            self.assertIn('name', item)
            self.assertIn('currency', item)
            self.assertIn('withdrawal_type', item)

    def test_payments_settings_usd_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(PaymentsSettings.CURRENCY_URL, currency='USD'),
                json=[{
                    'id': 11,
                    'name': 'some_name',
                    'currency': ['USD'],
                    'withdrawal_type': 'webmoney'
                }],
                status=200
            )

            result = self.client.PaymentsSettings.get(currency='USD')

        self.assertEqual(len(result), 1)
        for item in result:
            self.assertIn('id', item)
            self.assertIn('name', item)
            self.assertIn('currency', item)
            self.assertIn('withdrawal_type', item)


if __name__ == '__main__':
    unittest.main()

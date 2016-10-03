# coding: utf-8
from __future__ import unicode_literals

import unittest
import responses

from pyadmitad.items import StatisticWebsites, StatisticCampaigns,\
    StatisticDays, StatisticMonths, StatisticActions, StatisticSubIds,\
    StatisticSources, StatisticKeywords
from pyadmitad.constants import DEFAULT_PAGINATION_LIMIT, DEFAULT_PAGINATION_OFFSET
from pyadmitad.tests.base import BaseTestCase


class StatisticWebsitesTestCase(BaseTestCase):

    def test_get_statistic_websites_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticWebsites.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 20,
                    'subid': '1234567890987654321',
                    'total': 200,
                    'order_by': ['cr'],
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticWebsites.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=20,
                subid='1234567890987654321',
                total=200,
                order_by=['cr']
            )

        self.assertIn('status', result)


class StatisticCampaignTestCase(BaseTestCase):

    def test_get_statistic_campaign_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticCampaigns.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 20,
                    'subid': '1234567890987654321',
                    'total': 200,
                    'order_by': ['cr'],
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET

                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticCampaigns.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=20,
                subid='1234567890987654321',
                total=200,
                order_by=['cr']
            )

        self.assertIn('status', result)


class StatisticDaysTestCase(BaseTestCase):

    def test_get_statistic_days_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticDays.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 20,
                    'subid': '1234567890987654321',
                    'total': 200,
                    'order_by': ['cr'],
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET

                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticDays.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=20,
                subid='1234567890987654321',
                total=200,
                order_by=['cr']
            )

        self.assertIn('status', result)


class StatisticMonthsTestCase(BaseTestCase):

    def test_get_statistic_months_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticMonths.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 20,
                    'subid': '1234567890987654321',
                    'total': 200,
                    'order_by': ['cr'],
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticMonths.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=20,
                subid='1234567890987654321',
                total=200,
                order_by=['cr']
            )

        self.assertIn('status', result)


class StatisticActionsTestCase(BaseTestCase):

    def test_get_statistic_actions_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticActions.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'closing_date_start': '01.01.2010',
                    'closing_date_end': '01.02.2010',
                    'status_updated_start': '01.01.2010 10:10:10',
                    'status_updated_end': '01.02.2010 10:10:10',
                    'website': 10,
                    'campaign': 20,
                    'subid': '1234567890987654321',
                    'subid1': '1234567890987654321',
                    'subid4': '1234567890987654321',
                    'status': 1,
                    'keyword': 'foo',
                    'action': 'lead',
                    'action_type': 'lead',
                    'action_id': 27,
                    'order_by': ['status'],
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticActions.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                closing_date_start='01.01.2010',
                closing_date_end='01.02.2010',
                status_updated_start='01.01.2010 10:10:10',
                status_updated_end='01.02.2010 10:10:10',
                website=10,
                campaign=20,
                subid='1234567890987654321',
                subid1='1234567890987654321',
                subid4='1234567890987654321',
                status=1,
                keyword='foo',
                action='lead',
                action_type='lead',
                action_id=27,
                order_by=['status']
            )

        self.assertIn('status', result)


class StatisticSubIdsTestCase(BaseTestCase):

    def test_get_statistic_sub_ids_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticSubIds.URL, subid_number='', params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 20,
                    'subid1': '123567',
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticSubIds.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=20,
                subid1='123567'
            )

        self.assertIn('status', result)


class StatisticSourcesTestCase(BaseTestCase):

    def test_get_statistic_sources_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticSources.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 22,
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticSources.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=22
            )

        self.assertIn('status', result)


class StatisticKeywordsTestCase(BaseTestCase):

    def test_get_statistic_keywords_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(StatisticKeywords.URL, params={
                    'date_start': '01.01.2010',
                    'date_end': '01.02.2010',
                    'website': 10,
                    'campaign': 20,
                    'source': 'g',
                    'order_by': ['cr', 'ecpc'],
                    'limit': DEFAULT_PAGINATION_LIMIT,
                    'offset': DEFAULT_PAGINATION_OFFSET
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.StatisticKeywords.get(
                date_start='01.01.2010',
                date_end='01.02.2010',
                website=10,
                campaign=20,
                source='g',
                order_by=['cr', 'ecpc']
            )

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

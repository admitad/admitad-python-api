# coding: utf-8
from __future__ import unicode_literals

from copy import copy

from pyadmitad.constants import MAX_SUB_ID_LENGTH
from pyadmitad.items.base import Item


__all__ = [
    'StatisticWebsites',
    'StatisticCampaigns',
    'StatisticDays',
    'StatisticMonths',
    'StatisticActions',
    'StatisticSubIds',
    'StatisticSources',
    'StatisticKeywords',
]


class StatisticBase(Item):

    STATUSES = (1, 2, 3)
    SOURCES = ('g', 'y')
    ACTION_TYPES = ('lead', 'sale')

    ORDERING = (
        'action',
        'clicks',
        'cr',
        'ctr',
        'ecpc',
        'ecpm',
        'leads',
        'name',
        'payment_sum',
        'payment_sum_approved',
        'payment_sum_declined',
        'payment_sum_open',
        'sales',
        'views',
    )

    @staticmethod
    def check_sub_id(sub_id):
        return sub_id if len(sub_id) <= MAX_SUB_ID_LENGTH else None

    @staticmethod
    def check_sources(source):
        return source if source in StatisticBase.SOURCES else None,

    @staticmethod
    def check_status(status):
        return status if status in StatisticBase.STATUSES else None,

    @staticmethod
    def check_actions_type(action_type):
        return action_type if action_type in StatisticBase.ACTION_TYPES else None,

    FILTERING = {
        'date_start': lambda x: Item.sanitize_date(x, 'date_start', blank=True),
        'date_end': lambda x: Item.sanitize_date(x, 'date_end', blank=True),
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
        'total': lambda x: Item.sanitize_integer_value(x, 'total', blank=True),
        'subid': lambda x: StatisticBase.check_sub_id(x)
    }

    def get(self, url, **kwargs):
        """Base GET method"""
        kwargs['url'] = url

        ordering = {
            'order_by': kwargs.get('order_by', []),
            'available': self.ORDERING
        }

        filtering = {
            'filter_by': kwargs,
            'available': self.FILTERING,
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_ordering(ordering) \
                   .set_filtering(filtering) \
                   .request(**kwargs)


class StatisticWebsites(StatisticBase):
    """
    Statistics by websites

    """

    SCOPE = 'statistics'

    URL = Item.prepare_url('statistics/websites')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            website (int)
            campaign (int)
            subid (str)
            total (int)
            limit (int)
            offset (int)
            order_by (list of str)

        """
        return super(StatisticWebsites, self).get(self.URL, **kwargs)


class StatisticCampaigns(StatisticBase):
    """
    Statistics by campaigns

    """

    SCOPE = 'statistics'

    URL = Item.prepare_url('statistics/campaigns')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            website (int)
            campaign (int)
            subid (str)
            total (int)
            limit (int)
            offset (int)
            order_by (str)

        """
        return super(StatisticCampaigns, self).get(self.URL, **kwargs)


class StatisticDays(StatisticBase):
    """
    Statistics by days

    """

    SCOPE = 'statistics'

    URL = Item.prepare_url('statistics/dates')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            website (int)
            campaign (int)
            subid (str)
            total (int)
            limit (int)
            offset (int)
            order_by (str)

        """
        return super(StatisticDays, self).get(self.URL, **kwargs)


class StatisticMonths(StatisticBase):
    """
    Statistics by months

    """

    SCOPE = 'statistics'

    URL = Item.prepare_url('statistics/months')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            website (int)
            campaign (int)
            subid (str)
            total (int)
            limit (int)
            offset (int)
            order_by (str)

        """
        return super(StatisticMonths, self).get(self.URL, **kwargs)


class StatisticActions(StatisticBase):
    """
    Statistics by actions

    """

    SCOPE = 'statistics'

    ORDERING = (
        'action',
        'banner',
        'banner_id',
        'campaign',
        'cart',
        'click_date',
        'conv_time',
        'datetime',
        'payment',
        'status',
        'subid',
        'subid1',
        'subid2',
        'subid3',
        'subid4',
        'website'
    )

    FILTERING = {
        'date_start': lambda x: Item.sanitize_date(x, 'date_start', blank=True),
        'date_end': lambda x: Item.sanitize_date(x, 'date_end', blank=True),
        'closing_date_start': lambda x: Item.sanitize_date(x, 'closing_date_start', blank=True),
        'closing_date_end': lambda x: Item.sanitize_date(x, 'closing_date_end', blank=True),
        'status_updated_start': lambda x: Item.sanitize_long_date(x, 'status_updated_start', blank=True),
        'status_updated_end': lambda x: Item.sanitize_long_date(x, 'status_updated_end', blank=True),
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
        'subid': lambda x: StatisticBase.check_sub_id(x),
        'subid1': lambda x: StatisticBase.check_sub_id(x),
        'subid2': lambda x: StatisticBase.check_sub_id(x),
        'subid3': lambda x: StatisticBase.check_sub_id(x),
        'subid4': lambda x: StatisticBase.check_sub_id(x),
        'source': lambda x: StatisticBase.check_sources(x),
        'status': lambda x: StatisticBase.check_status(x),
        'keyword': lambda x: Item.sanitize_string_value(x, 'keyword', blank=True),
        'action': lambda x: Item.sanitize_string_value(x, 'action', blank=True),
        'action_type': lambda x: StatisticBase.check_actions_type(x),
        'action_id': lambda x: Item.sanitize_integer_value(x, 'action_id', blank=True),
    }

    URL = Item.prepare_url('statistics/actions')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            closing_date_start (date)
            closing_date_end (date)
            status_updated_start (date)
            status_updated_end (date)
            website (int)
            campaign (int)
            subid (str)
            subid1 (str)
            subid2 (str)
            subid3 (str)
            subid4 (str)
            source (str)
            status (int)
            keyword (str)
            action (str)
            action_type (str)
            action_id (int)
            limit (int)
            offset (int)
            order_by (list of int)

        """
        return super(StatisticActions, self).get(self.URL, **kwargs)


class StatisticSubIds(StatisticBase):
    """
    Statistics by sub-ids

    """

    SCOPE = 'statistics'

    SUB_ID_NUMBERS = range(0, 5)

    ORDERING = (
        'actions',
        'clicks',
        'cr',
        'ecpc',
        'leads',
        'payment_sum',
        'payment_sum_approved',
        'payment_sum_declined',
        'payment_sum_open',
        'sales'
    )

    FILTERING = {
        'date_start': lambda x: Item.sanitize_date(x, 'date_start', blank=True),
        'date_end': lambda x: Item.sanitize_date(x, 'date_end', blank=True),
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
    }

    URL = Item.prepare_url('statistics/sub_ids%(subid_number)s')

    def sanitize_sub_id_number(self, number):
        if number not in self.SUB_ID_NUMBERS:
            raise ValueError("Invalid subid number. '%s': %s" % (number, self.SUB_ID_NUMBERS))

    def prepare_filtering(self, sub_id_number):
        params = copy(self.FILTERING)
        subid_params = dict([
            ('subid%s' % (val or ''), StatisticBase.check_sub_id)
            for val in self.SUB_ID_NUMBERS if val != sub_id_number])
        params.update(subid_params)
        return params

    def prepare_ordering(self, sub_id_number):
        sub_id_name = 'subid%s' % (sub_id_number or '')
        return self.ORDERING + (sub_id_name,)

    def get(self, sub_id_number=0, **kwargs):
        """
        Here sub_id_number is subid number.
        It is allowed from 0 to 5 excluding.
        It just will send request to sub_ids, sub_ids1, sub_ids2,
         sub_ids3, sub_ids4 urls correspondingly.

        res = client.StatisticSubIds.get()
        res = client.StatisticSubIds.get(date_start='01.01.2013')
        res = client.StatisticSubIds.get(subid="ADS778")
        res = client.StatisticSubIds.get(subid1="ADS778", sub_id_number=2)
        res = client.StatisticSubIds.get(limit=2)

        """
        self.sanitize_sub_id_number(sub_id_number)
        kwargs['url'] = self.URL % {
            'subid_number': sub_id_number or ''
        }

        ordering = {
            'order_by': kwargs.get('order_by', []),
            'available': self.prepare_ordering(sub_id_number)
        }

        filtering = {
            'filter_by': kwargs,
            'available': self.prepare_filtering(sub_id_number)
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_ordering(ordering) \
                   .set_filtering(filtering) \
                   .request(**kwargs)


class StatisticSources(StatisticBase):
    """
    Statistics by sources

    """

    SCOPE = 'statistics'

    ORDERING = (
        'actions',
        'clicks',
        'cr',
        'ecpc',
        'leads',
        'payment_sum',
        'payment_sum_approved',
        'payment_sum_declined',
        'payment_sum_open',
        'sales',
        'source',
    )

    FILTERING = {
        'date_start': lambda x: Item.sanitize_date(x, 'date_start', blank=True),
        'date_end': lambda x: Item.sanitize_date(x, 'date_end', blank=True),
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
    }

    URL = Item.prepare_url('statistics/sources')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            website (int)
            campaign (int)
            limit (int)
            offset (int)
            order_by (list of int)

        """
        return super(StatisticSources, self).get(self.URL, **kwargs)


class StatisticKeywords(StatisticBase):
    """
    Statistics by keywords

    """

    SCOPE = 'statistics'

    ORDERING = (
        'actions',
        'clicks',
        'cr',
        'ecpc',
        'keyword',
        'leads',
        'payment_sum',
        'payment_sum_approved',
        'payment_sum_declined',
        'payment_sum_open',
        'sales',
        'source',
    )

    FILTERING = {
        'date_start': lambda x: Item.sanitize_date(x, 'date_start', blank=True),
        'date_end': lambda x: Item.sanitize_date(x, 'date_end', blank=True),
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
        'source': StatisticBase.check_sources,
    }

    URL = Item.prepare_url('statistics/keywords')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            website (int)
            campaign (int)
            source (str)
            limit (int)
            offset (int)
            order_by (list of str)

        """
        return super(StatisticKeywords, self).get(self.URL, **kwargs)

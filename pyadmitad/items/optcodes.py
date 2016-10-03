# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'OptCodes',
    'OfferStatusOptCodesManager',
    'ActionOptCodesManager',
]


class BaseOptCodes(Item):

    DESC_MODE_SIMPLE = 0
    DESC_MODE_EXTENDED = 1

    METHOD_GET = 0
    METHOD_POST = 1

    ACTION_TYPE_ALL = 0
    ACTION_TYPE_SALE = 1
    ACTION_TYPE_LEAD = 2

    ACTION_STATUS_NEW = 5
    ACTION_STATUS_APPROVED = 6
    ACTION_STATUS_DECLINED = 7
    ACTION_STATUS_PENDING = 8

    EVENT_ACTION = 0
    EVENT_OFFER_STATUS = 1
    EVENT_REFERRAL = 2


class OptCodes(BaseOptCodes):

    SCOPE = 'opt_codes'

    ORDERING = ('action_type', 'method', 'desc_mode')

    URL = Item.prepare_url('opt_codes')
    SINGLE_URL = Item.prepare_url('opt_codes/%(optcode_id)s')

    def get(self, **kwargs):
        """
        Args:
            campaign (int)
            website (int)
            limit (int)
            offset (int)
            order_by (list of str)

        """
        ordering = {
            'order_by': kwargs.get('order_by', []),
            'available': self.ORDERING
        }

        filtering = {
            'filter_by': kwargs,
            'available': {
                'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
                'website': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_ordering(ordering) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, optcode_id, **kwargs):
        """
        Args:
            optcode_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'optcode_id': Item.sanitize_id(optcode_id)
        }

        return self.transport.get().request(**request_data)


class BaseOptCodesManager(BaseOptCodes):

    SCOPE = 'manage_opt_codes'

    DELETE_URL = Item.prepare_url('opt_codes/delete/%(optcode_id)s')
    CREATE_URL = ''
    UPDATE_URL = ''

    CREATE_FIELDS = {}
    UPDATE_FIELDS = {}

    def delete(self, optcode_id):
        request_data = {
            'url': self.DELETE_URL,
            'optcode_id': Item.sanitize_id(optcode_id),
        }
        return self.transport.post().request(**request_data)

    def create(self, **kwargs):
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)
        return self.transport.post().set_data(data).request(url=self.CREATE_URL)

    def update(self, optcode_id, **kwargs):
        data = Item.sanitize_fields(self.UPDATE_FIELDS, **kwargs)
        request_data = {
            'url': self.UPDATE_URL,
            'optcode_id': Item.sanitize_id(optcode_id),
        }

        return self.transport.post().set_data(data).request(**request_data)


class OfferStatusOptCodesManager(BaseOptCodesManager):

    CREATE_URL = Item.prepare_url('opt_codes/offer/create')
    UPDATE_URL = Item.prepare_url('opt_codes/offer/update/%(optcode_id)s')

    CREATE_FIELDS = {
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
        'desc_mode': lambda x: Item.sanitize_integer_value(x, 'desc_mode'),
        'url': lambda x: Item.sanitize_string_value(x, 'url'),
        'method': lambda x: Item.sanitize_integer_value(x, 'method'),
    }
    UPDATE_FIELDS = {
        'desc_mode': lambda x: Item.sanitize_integer_value(x, 'desc_mode', blank=True),
        'url': lambda x: Item.sanitize_string_value(x, 'url', blank=True),
        'method': lambda x: Item.sanitize_integer_value(x, 'method', blank=True),
    }


class ActionOptCodesManager(BaseOptCodesManager):

    CREATE_URL = Item.prepare_url('opt_codes/action/create')
    UPDATE_URL = Item.prepare_url('opt_codes/action/update/%(optcode_id)s')

    CREATE_FIELDS = {
        'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
        'desc_mode': lambda x: Item.sanitize_integer_value(x, 'desc_mode'),
        'url': lambda x: Item.sanitize_string_value(x, 'url'),
        'method': lambda x: Item.sanitize_integer_value(x, 'method'),
        'action_type': lambda x: Item.sanitize_integer_value(x, 'action_type'),
        'status': lambda x: Item.sanitize_integer_value(x, 'status'),
    }
    UPDATE_FIELDS = {
        'desc_mode': lambda x: Item.sanitize_integer_value(x, 'desc_mode', blank=True),
        'url': lambda x: Item.sanitize_string_value(x, 'url', blank=True),
        'method': lambda x: Item.sanitize_integer_value(x, 'method', blank=True),
        'action_type': lambda x: Item.sanitize_integer_value(x, 'action_type', blank=True),
        'status': lambda x: Item.sanitize_integer_value(x, 'status', blank=True),
    }

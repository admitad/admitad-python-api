# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Payments',
    'PaymentsStatement',
    'PaymentsManage',
]


class Payments(Item):
    """
    List of webmaster payments

    """

    SCOPE = 'payments'

    URL = Item.prepare_url('payments')
    SINGLE_URL = Item.prepare_url('payments/%(payment_id)s')

    def get(self, **kwargs):
        """
        Args:
            has_statement (bool)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'has_statement': lambda x: Item.sanitize_bool_integer_value(x, 'has_statement', blank=True)
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, _id, **kwargs):
        """
        Args:
            _id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'payment_id': Item.sanitize_id(_id)
        }

        return self.transport.get().request(**request_data)


class PaymentsStatement(Item):

    SCOPE = 'payments'

    URL = Item.prepare_url('payments/%(payment_id)s/statement')

    def get(self, payment_id, **kwargs):
        """
        Args:
            detailed (bool)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'detailed': lambda x: Item.sanitize_bool_integer_value(x, 'detailed', blank=True)
            }
        }

        request_data = {
            'url': self.URL,
            'payment_id': Item.sanitize_id(payment_id)
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(**request_data)


class PaymentsManage(Item):
    """
    Manage payments

    """

    SCOPE = 'manage_payments'

    CREATE_URL = Item.prepare_url('payments/request/%(code)s')
    CONFIRM_URL = Item.prepare_url('payments/confirm/%(payment_id)s')
    DELETE_URL = Item.prepare_url('payments/delete/%(payment_id)s')

    def create(self, _code, **kwargs):
        """
        Create a payment request.
        _code is a code of currency

        Args:
            _code (str)

        """
        request_data = {
            'url': self.CREATE_URL,
            'code': Item.sanitize_currency_value(_code)
        }

        return self.transport.post().request(**request_data)

    def confirm(self, _id, **kwargs):
        """
        Confirm a payment request.
        _id is a payment id.

        Args:
            _id (int)

        """
        request_data = {
            'url': self.CONFIRM_URL,
            'payment_id': Item.sanitize_id(_id)
        }

        return self.transport.post().request(**request_data)

    def delete(self, _id, **kwargs):
        """
        Delete a payment request.
        _id is a payment id.

        Args:
            _id (int)

        """
        request_data = {
            'url': self.DELETE_URL,
            'payment_id': Item.sanitize_id(_id)
        }

        return self.transport.post().request(**request_data)

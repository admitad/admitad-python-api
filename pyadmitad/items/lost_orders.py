# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'LostOrders',
    'LostOrdersManager',
]


class LostOrders(Item):

    SCOPE = 'lost_orders'

    URL = Item.prepare_url('lost_orders')
    SINGLE_URL = Item.prepare_url('lost_orders/%(lost_order_id)s')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """
        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)

    def getOne(self, lost_order_id):
        """
        Args:
            lost_order_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'lost_order_id': Item.sanitize_id(lost_order_id)
        }

        return self.transport.get().request(**request_data)


class LostOrdersManager(Item):

    SCOPE = 'manage_lost_orders'

    DELETE_URL = Item.prepare_url('lost_orders/%(lost_order_id)s/decline')
    CREATE_URL = Item.prepare_url('lost_orders/create')

    CREATE_FIELDS = {
        'advcampaign': lambda x: Item.sanitize_integer_value(x, 'advcampaign'),
        'website': lambda x: Item.sanitize_integer_value(x, 'website'),
        'order_id': lambda x: Item.sanitize_string_value(x, 'order_id'),
        'order_date': lambda x: Item.sanitize_date(x, 'order_date'),
        'order_price': lambda x: Item.sanitize_float_value(x, 'order_price'),
        'comment': lambda x: Item.sanitize_string_value(x, 'comment'),
    }

    def delete(self, lost_order_id):
        """
        Args:
            lost_order_id (int)

        """
        request_data = {
            'url': self.DELETE_URL,
            'lost_order_id': Item.sanitize_id(lost_order_id),
        }

        return self.transport.delete().request(**request_data)

    def create(self, attachments, **kwargs):
        """
        Args:
            attachments (list of str)
            advcampaign (int)
            website (int)
            order_id (str)
            order_date (date)
            order_price (float)
            comment (str)

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)
        files = [('attachment', open(item, 'rb')) for item in Item.sanitize_string_array(attachments, 'attachments')]

        return self.transport.post().set_data(data).set_files(files).request(url=self.CREATE_URL)

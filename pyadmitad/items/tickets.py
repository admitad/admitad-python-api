# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Tickets',
    'TicketsManager'
]


class Tickets(Item):
    SCOPE = 'tickets'

    URL = Item.prepare_url('tickets')
    SINGLE_URL = Item.prepare_url('tickets/%(ticket_id)s')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            status (int)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'date_start': lambda x: Item.sanitize_date(x, 'date_start', True),
                'date_end': lambda x: Item.sanitize_date(x, 'date_end', True),
                'status': lambda x: Item.sanitize_integer_value(x, 'status', True),
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, ticket_id):
        """
        Args:
            ticket_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'ticket_id': Item.sanitize_id(ticket_id)
        }

        return self.transport.get().request(**request_data)


class TicketsManager(Item):

    SCOPE = 'manage_tickets'

    CREATE_URL = Item.prepare_url('tickets/create')
    COMMENT_URL = Item.prepare_url('tickets/%(ticket_id)s/create')

    CREATE_FIELDS = {
        'subject': lambda x: Item.sanitize_string_value(x, 'subject'),
        'text': lambda x: Item.sanitize_string_value(x, 'text'),
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign'),
        'category': lambda x: Item.sanitize_integer_value(x, 'category'),
        'priority': lambda x: Item.sanitize_integer_value(x, 'priority'),
    }

    COMMENT_FIELDS = {
        'text': lambda x: Item.sanitize_string_value(x, 'text'),
    }

    def create(self, **kwargs):
        """
        Args:
            subject (str)
            text (str)
            campaign (int)
            category (int)
            priority (int)

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)

        return self.transport.post().set_data(data).request(url=self.CREATE_URL)

    def comment(self, ticket_id, **kwargs):
        """
        Args:
            ticket_id (int)
            text (str)

        """
        request_data = {
            'url': self.COMMENT_URL,
            'ticket_id': Item.sanitize_id(ticket_id)
        }

        data = Item.sanitize_fields(self.COMMENT_FIELDS, **kwargs)

        return self.transport.post().set_data(data).request(**request_data)

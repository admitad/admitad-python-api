# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'BrokenLinks',
    'ManageBrokenLinks'
]


class BrokenLinks(Item):

    SCOPE = 'broken_links'

    URL = Item.prepare_url('broken_links')
    SINGLE_URL = Item.prepare_url('broken_links/%(broken_link_id)s')

    def get(self, **kwargs):
        """
        Args:
            website (list of int)
            campaign (list of int)
            search (str)
            reason (int)
            date_start (date)
            date_end (date)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'website': lambda x: Item.sanitize_integer_array(x, 'website', blank=True),
                'campaign': lambda x: Item.sanitize_integer_array(x, 'campaign', blank=True),
                'search': lambda x: Item.sanitize_string_value(x, 'search', blank=True),
                'reason': lambda x: Item.sanitize_integer_value(x, 'reason', blank=True),
                'date_start': lambda x: Item.sanitize_date(x, 'date_start', blank=True),
                'date_end': lambda x: Item.sanitize_date(x, 'date_end', blank=True),
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, broken_link_id):
        """
        Args:
            broken_link_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'broken_link_id': Item.sanitize_id(broken_link_id)
        }

        return self.transport.get().request(**request_data)


class ManageBrokenLinks(Item):

    SCOPE = 'manage_broken_links'

    RESOLVE_URL = Item.prepare_url('broken_links/resolve')

    def resolve(self, broken_link_ids):
        """
        Args:
            broken_links_ids (list of int)

        """

        filtering = {
            'filter_by': {
                'link_id': broken_link_ids
            },
            'available': {
                'link_id': lambda x: Item.sanitize_integer_array(x, 'link_id', blank=True)
            }
        }

        return self.transport.post() \
                   .set_filtering(filtering) \
                   .request(url=self.RESOLVE_URL)

# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Arecords'
]


class Arecords(Item):

    SCOPE = 'arecords'

    URL = Item.prepare_url('arecords')
    FOR_WEBSITE_URL = Item.prepare_url('arecords/%(website_id)s')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """

        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)

    def getForWebsite(self, website_id, **kwargs):
        """
        Args:
            website_id (int)

        """

        request_data = {
            'url': self.FOR_WEBSITE_URL,
            'website_id': Item.sanitize_id(website_id)
        }

        return self.transport.get().request(**request_data)

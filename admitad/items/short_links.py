# coding: utf-8
from __future__ import unicode_literals

from admitad.items.base import Item


__all__ = [
    'ShortLinks'
]


class ShortLinks(Item):

    SCOPE = 'short_links'

    URL = Item.prepare_url('shortlink/modify/')

    GET_FIELDS = {
        'link': lambda x: Item.sanitize_string_value(x, 'link'),
    }

    def post(self, link, **kwargs):
        """
        Args:
            link (str)

        """
        data = Item.sanitize_fields(self.GET_FIELDS, link=link)

        return self.transport.post().set_data(data).request(url=self.URL)

# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


class LinksValidator(Item):

    SCOPE = 'validate_links'

    URL = Item.prepare_url('validate_links')

    GET_FIELDS = {
        'link': lambda x: Item.sanitize_string_value(x, 'link'),
    }

    def get(self, link, **kwargs):
        """
        Args:
            link (str)

        """
        data = Item.sanitize_fields(self.GET_FIELDS, link=link)

        return self.transport.get().set_data(data).request(url=self.URL)

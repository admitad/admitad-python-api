# coding: utf-8
from __future__ import unicode_literals

from admitad.items.base import Item


__all__ = (
    'SubnetworksWebsitesManageV1',
)


class SubnetworksWebsitesManageV1(Item):
    """
    Manage websites using subnetworks v1 API

    """

    SCOPE = 'manage_websites'
    CREATE_URL = Item.prepare_url('subnetworks/v1/websites/create')

    CREATE_FIELDS = {
        'name': lambda x: Item.sanitize_string_value(x, 'name', max_length=200),
        'native_kind': lambda x: Item.sanitize_string_value(x, 'native_kind', max_length=64, blank=True),
        'url': lambda x: Item.sanitize_string_value(x, 'url', max_length=255),
        'category': lambda x: Item.sanitize_integer_array(x, 'category'),
        'region': lambda x: Item.sanitize_string_array(x, 'region'),
    }

    def create(self, **kwargs):
        """
        Args:
            name (str) - website name
            native_kind (str) - platform kind for subnetwork website
            url (str) - website url
            category (list of int) - website categories
            region (list of str) - website regions

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)
        return self.transport.post().set_data(data).request(url=self.CREATE_URL)

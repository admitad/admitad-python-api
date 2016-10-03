# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'DeeplinksManage',
]


class DeeplinksManage(Item):

    SCOPE = 'deeplink_generator'

    CREATE_URL = Item.prepare_url('deeplink/%(website_id)s/advcampaign/%(campaign_id)s')

    CREATE_FIELDS = {
        'ulp': lambda x: Item.sanitize_string_value(x, 'ulp'),
        'subid': lambda x: Item.sanitize_string_value(x, 'subid', max_length=30),
        # todo: subid[1-4]
    }

    def create(self, website_id, campaign_id, **kwargs):
        """
        Args:
            website_id (int)
            campaign_id (int)
            ulp (str)
            subid (str)

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)

        request_data = {
            'url': self.CREATE_URL,
            'website_id': Item.sanitize_id(website_id),
            'campaign_id': Item.sanitize_id(campaign_id),
        }

        return self.transport.get().set_data(data).request(**request_data)

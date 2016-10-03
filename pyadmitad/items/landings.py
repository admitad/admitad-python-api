# coding:  utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Landings',
    'LandingsForWebsite',
]


class Landings(Item):

    SCOPE = 'landings'

    URL = Item.prepare_url('landings/%(campaign_id)s')

    def get(self, campaign_id, **kwargs):
        """
        Args:
            campaign_id (int)
            limit (int)
            offset (int)

        """
        request_data = {
            'url': self.URL,
            'campaign_id': Item.sanitize_id(campaign_id),
        }

        return self.transport.get().set_pagination(**kwargs).request(**request_data)


class LandingsForWebsite(Item):

    SCOPE = 'landings'

    URL = Item.prepare_url('landings/%(campaign_id)s/website/%(website_id)s')

    def get(self, campaign_id, website_id, **kwargs):
        """
        Args:
            campaign_id (int)
            website_id (int)
            limit (int)
            offset (int)

        """
        request_data = {
            'url': self.URL,
            'campaign_id': Item.sanitize_id(campaign_id),
            'website_id': Item.sanitize_id(website_id),
        }

        return self.transport.get().set_pagination(**kwargs).request(**request_data)

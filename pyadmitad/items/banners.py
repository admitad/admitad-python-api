# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Banners',
    'BannersForWebsite',
]


class Banners(Item):
    """
    List of banners

    """

    SCOPE = 'banners'

    URL = Item.prepare_url('banners/%(campaign_id)s')

    def get(self, _id, **kwargs):
        """
        Here _id is an id of advertising campaign

        Args:
            _id (int)
            mobile_content (bool)
            limit (int)
            offset(int)

        """
        request_data = {
            'url': self.URL,
            'campaign_id': Item.sanitize_id(_id)
        }

        filtering = {
            'filter_by': kwargs,
            'available': {
                'mobile_content': lambda x: Item.sanitize_bool_value(x, blank=True)
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(**request_data)


class BannersForWebsite(Item):
    """
    List of banners for the website

    """

    SCOPE = 'banners_for_website'

    URL = Item.prepare_url('banners/%(campaign_id)s/website/%(website_id)s')

    def get(self, _id, w_id, **kwargs):
        """
        Here _id is an id of advertising campaign and
        w_id is a id of website

        Args:
            _id (int)
            w_id (int)
            mobile_content (bool)
            landing (int)
            uri_scheme (str)
            limit (int)
            offset (int)

        """
        request_data = {
            'url': self.URL,
            'campaign_id': Item.sanitize_id(_id),
            'website_id': Item.sanitize_id(w_id)
        }

        filtering = {
            'filter_by': kwargs,
            'available': {
                'mobile_content': lambda x: Item.sanitize_bool_value(x, blank=True),
                'landing': lambda x: Item.sanitize_integer_value(x, 'landing', blank=True),
                'uri_scheme': lambda x: Item.sanitize_string_value(x, 'uri_scheme', blank=True)
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(**request_data)

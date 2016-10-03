# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Campaigns',
    'CampaignsForWebsite',
    'CampaignsManage',
]


class Campaigns(Item):
    """
    List of advertising campaigns

    """

    SCOPE = 'advcampaigns'

    URL = Item.prepare_url('advcampaigns')
    SINGLE_URL = Item.prepare_url('advcampaigns/%(campaign_id)s')

    def get(self, **kwargs):
        """
        Args:
            website (int)
            has_tool (list of str)
            limit (int)
            offset (int)
            language (str)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
                'has_tool': lambda x: Item.sanitize_string_array(x, 'has_tool', blank=True),
                'language': lambda x: Item.sanitize_string_value(x, 'language', blank=True),
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, _id, **kwargs):
        """
        Here _id is an a campaign id

        Args:
            _id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'campaign_id': Item.sanitize_id(_id)
        }

        return self.transport.get().request(**request_data)


class CampaignsForWebsite(Item):
    """
    List of advertising campaigns for a website

    """

    SCOPE = 'advcampaigns_for_website'

    URL = Item.prepare_url('advcampaigns/website/%(website_id)s')
    SINGLE_URL = Item.prepare_url('advcampaigns/%(campaign_id)s/website/%(website_id)s')

    def get(self, _id, **kwargs):
        """
        Here _id is a website id

        Args:
            _id (int)
            limit (int)
            offset (int)

        """
        request_data = {
            'url': self.URL,
            'website_id': Item.sanitize_id(_id)
        }

        return self.transport.get().set_pagination(**kwargs).request(**request_data)

    def getOne(self, _id, c_id, **kwargs):
        """
        Here _id is a website id and c_id is a campaign id

        Args:
            _id (int)
            c_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'website_id': Item.sanitize_id(_id),
            'campaign_id': Item.sanitize_id(c_id)
        }

        return self.transport.get().request(**request_data)


class CampaignsManage(Item):
    """
    Manage an advertising campaign

    """

    SCOPE = 'manage_advcampaigns'

    CONNECT_URL = Item.prepare_url('advcampaigns/%(campaign_id)s/attach/%(website_id)s')
    DISCONNECT_URL = Item.prepare_url('advcampaigns/%(campaign_id)s/detach/%(website_id)s')

    def connect(self, c_id, w_id, **kwargs):
        """
        Connect an advertising campaign for a website
        Here w_id is a website id and c_id is a campaign id

        Args:
            c_id (int)
            w_id (int)

        """
        request_data = {
            'url': self.CONNECT_URL,
            'campaign_id': Item.sanitize_id(c_id),
            'website_id': Item.sanitize_id(w_id)
        }

        return self.transport.post().request(**request_data)

    def disconnect(self, c_id, w_id, **kwargs):
        """
        Disconnect an advertising campaign from a website
        Here w_id is a website id and c_id is a campaign id

        Args:
            c_id (int)
            w_id (int)

        """
        request_data = {
            'url': self.DISCONNECT_URL,
            'campaign_id': Item.sanitize_id(c_id),
            'website_id': Item.sanitize_id(w_id)
        }

        return self.transport.post().request(**request_data)

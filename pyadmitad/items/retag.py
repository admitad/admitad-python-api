# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Retag',
    'RetagManager'
]


class Retag(Item):
    SCOPE = 'webmaster_retag'

    URL = Item.prepare_url('retag')
    SINGLE_URL = Item.prepare_url('retag/%(retag_id)s')
    LEVELS_FOR_WEBSITE_URL = Item.prepare_url('retag/website/%(website_id)s/levels')
    LEVELS_FOR_CAMPAIGN_URL = Item.prepare_url('retag/advcampaign/%(campaign_id)s/levels')

    def get(self, **kwargs):
        """
        Args:
            website (int)
            active (bool)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'website': lambda x: Item.sanitize_integer_value(x, 'website', True),
                'active': lambda x: Item.sanitize_bool_integer_value(x, 'active', True)
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, retag_id):
        """
        Args:
            retag_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'retag_id': Item.sanitize_id(retag_id)
        }

        return self.transport.get().request(**request_data)

    def getLevelsForWebsite(self, website_id):
        """
        Args:
            website_id (int)

        """
        request_data = {
            'url': self.LEVELS_FOR_WEBSITE_URL,
            'website_id': Item.sanitize_id(website_id)
        }

        return self.transport.get().request(**request_data)

    def getLevelsForCampaign(self, campaign_id):
        """
        Args:
            capaign_id (int)

        """
        request_data = {
            'url': self.LEVELS_FOR_CAMPAIGN_URL,
            'campaign_id': Item.sanitize_id(campaign_id)
        }

        return self.transport.get().request(**request_data)


class RetagManager(Item):

    SCOPE = 'manage_webmaster_retag'

    CREATE_URL = Item.prepare_url('retag/create')
    UPDATE_URL = Item.prepare_url('retag/update/%(retag_id)s')
    DELETE_URL = Item.prepare_url('retag/delete/%(retag_id)s')

    CREATE_FIELDS = {
        'website': lambda x: Item.sanitize_integer_value(x, 'website'),
        'level': lambda x: Item.sanitize_integer_value(x, 'level'),
        'active': lambda x: Item.sanitize_bool_integer_value(x, 'active', blank=True),
        'script': lambda x: Item.sanitize_string_value(x, 'script'),
        'comment': lambda x: Item.sanitize_string_value(x, 'comment', blank=True),
    }

    UPDATE_FIELDS = {
        'level': lambda x: Item.sanitize_integer_value(x, 'level', blank=True),
        'active': lambda x: Item.sanitize_bool_integer_value(x, 'active', blank=True),
        'script': lambda x: Item.sanitize_string_value(x, 'script', blank=True),
        'comment': lambda x: Item.sanitize_string_value(x, 'comment', blank=True),
    }

    def create(self, **kwargs):
        """
        Args:
            website (int)
            level (int)
            active (bool)
            script (str)
            comment (str)

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)

        return self.transport.post().set_data(data).request(url=self.CREATE_URL)

    def update(self, retag_id, **kwargs):
        """
        Args:
            retag_id (int)
            level (int)
            active (bool)
            script (str)
            comment (str)

        """
        request_data = {
            'url': self.UPDATE_URL,
            'retag_id': Item.sanitize_id(retag_id)
        }

        data = Item.sanitize_fields(self.UPDATE_FIELDS, **kwargs)

        return self.transport.post().set_data(data).request(**request_data)

    def delete(self, retag_id):
        """
        Args:
            retag_id (int)

        """
        request_data = {
            'url': self.DELETE_URL,
            'retag_id': Item.sanitize_id(retag_id)
        }

        return self.transport.post().request(**request_data)

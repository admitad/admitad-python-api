# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = (
    'Websites',
    'WebsitesManage'
)


class Websites(Item):
    """
    List of websites

    """

    SCOPE = 'websites'

    URL = Item.prepare_url('websites')
    SINGLE_URL = Item.prepare_url('websites/%(website_id)s')

    STATUS_NEW = 'new'
    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_DECLINED = 'declined'

    CAMPAIGN_STATUS_PENDING = 'pending'
    CAMPAIGN_STATUS_ACTIVE = 'active'
    CAMPAIGN_STATUS_DECLINED = 'declined'
    CAMPAIGN_STATUS_DISABLED = 'disabled'

    STATUS_LIST = [
        STATUS_NEW, STATUS_PENDING, STATUS_ACTIVE,
        STATUS_SUSPENDED, STATUS_DECLINED
    ]
    CAMPAIGN_STATUS_LIST = [
        CAMPAIGN_STATUS_PENDING, CAMPAIGN_STATUS_ACTIVE,
        CAMPAIGN_STATUS_DECLINED, CAMPAIGN_STATUS_DISABLED
    ]

    def get(self, **kwargs):
        """
        Args:
            status (str)
            campaign_status (str)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'status': lambda x: x if x in self.STATUS_LIST else None,
                'campaign_status': lambda x: x if x in self.CAMPAIGN_STATUS_LIST else None
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, _id, **kwargs):
        """
        Args:
            _id (int)

        """
        requests_data = {
            'url': self.SINGLE_URL,
            'website_id': Item.sanitize_id(_id)
        }

        return self.transport.get().request(**requests_data)


class WebsitesManage(Item):
    """
    Manage websites

    """

    SCOPE = 'manage_websites'

    CREATE_URL = Item.prepare_url('website/create')
    UPDATE_URL = Item.prepare_url('website/update/%(website_id)s')
    VERIFY_URL = Item.prepare_url('website/verify/%(website_id)s')
    DELETE_URL = Item.prepare_url('website/delete/%(website_id)s')

    CREATE_FIELDS = {
        'name': lambda x: Item.sanitize_string_value(
            x, 'name', max_length=200),
        'kind': lambda x: Item.sanitize_string_value(
            x, 'kind', max_length=20),
        'language': lambda x: Item.sanitize_string_value(
            x, 'language', max_length=2),
        'adservice': lambda x: Item.sanitize_integer_value(
            x, 'adservice', blank=True),
        'site_url': lambda x: Item.sanitize_string_value(
            x, 'site_url', max_length=255),
        'description': lambda x: Item.sanitize_string_value(
            x, 'description', max_length=20000, min_length=100),
        'categories': lambda x: Item.sanitize_integer_array(
            x, 'categories'),
        'regions': lambda x: Item.sanitize_string_array(
            x, 'regions', max_length=2),
        'atnd_visits': lambda x: Item.sanitize_integer_value(
            x, 'atnd_visits', blank=False),
        'atnd_hits': lambda x: Item.sanitize_integer_value(
            x, 'atnd_hits', blank=False),
        'mailing_targeting': lambda x: Item.sanitize_bool_integer_value(
            x, 'mailing_targeting', blank=True)
    }

    UPDATE_FIELDS = {
        'name': lambda x: Item.sanitize_string_value(
            x, 'name', max_length=200, blank=True),
        'language': lambda x: Item.sanitize_string_value(
            x, 'language', max_length=2, blank=True),
        'adservice': lambda x: Item.sanitize_integer_value(
            x, 'adservice', blank=True),
        'site_url': lambda x: Item.sanitize_string_value(
            x, 'site_url', max_length=255, blank=True),
        'description': lambda x: Item.sanitize_string_value(
            x, 'description', max_length=20000, min_length=100, blank=True),
        'categories': lambda x: Item.sanitize_integer_array(
            x, 'categories', blank=True),
        'regions': lambda x: Item.sanitize_string_array(
            x, 'regions', max_length=2, blank=True),
        'atnd_visits': lambda x: Item.sanitize_integer_value(
            x, 'atnd_visits', blank=True),
        'atnd_hits': lambda x: Item.sanitize_integer_value(
            x, 'atnd_hits', blank=True),
        'mailing_targeting': lambda x: Item.sanitize_bool_integer_value(
            x, 'mailing_targeting', blank=True)
    }

    def create(self, **kwargs):
        """
        Args:
            name (str)
            kind (str)
            language (str)
            adservice (int)
            site_url (str)
            description (str)
            categories (list of int)
            regions (list of str)
            atnd_visits (int)
            atnd_hits (int)
            mailing_targeting (bool)

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)

        return self.transport.post().set_data(data).request(url=self.CREATE_URL)

    def update(self, _id, **kwargs):
        """
        Args:
            _id (int)
            name (str)
            language (str)
            adservice (int)
            site_url (str)
            description (str)
            categories (list of int)
            regions (list of str)
            atnd_visits (int)
            atnd_hits (int)
            mailing_targeting (bool)

        """
        data = Item.sanitize_fields(self.UPDATE_FIELDS, **kwargs)

        request_data = {
            'url': self.UPDATE_URL,
            'website_id': Item.sanitize_id(_id)
        }

        return self.transport.post().set_data(data).request(**request_data)

    def verify(self, _id):
        """
        Args:
            _id (int)

        """
        request_data = {
            'url': self.VERIFY_URL,
            'website_id': Item.sanitize_id(_id)
        }

        return self.transport.post().request(**request_data)

    def delete(self, _id):
        """
        Args:
            _id (int)

        """
        request_data = {
            'url': self.DELETE_URL,
            'website_id': Item.sanitize_id(_id)
        }

        return self.transport.post().request(**request_data)

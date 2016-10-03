# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = (
    'WebsiteTypes',
    'WebsiteRegions',
    'SystemLanguages',
    'SystemCurrencies',
    'AdvertiserServices',
    'CampaignCategories',
)


class WebsiteTypes(Item):
    """
    List of websites types

    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('websites/kinds')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """

        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)


class WebsiteRegions(Item):
    """
    List of websites regions

    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('websites/regions')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """

        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)


class SystemLanguages(Item):
    """
    List of system languages

    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('languages')
    SINGLE_URL = Item.prepare_url('languages/%(code)s')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """

        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)

    def getOne(self, code='ru'):
        """
        Args:
            code (str)

        """

        request_data = {
            'url': self.SINGLE_URL,
            'code': Item.sanitize_string_value(code, 'code', 2, 2, False)
        }

        return self.transport.get().request(**request_data)


class SystemCurrencies(Item):
    """
    List of system currencies

    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('currencies')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """

        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)


class AdvertiserServices(Item):
    """
    List of advertiser services

    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('adservices')
    SINGLE_URL = Item.prepare_url('adservices/%(id)s')
    KIND_URL = Item.prepare_url('adservices/kind/%(kind)s')
    KIND_SINGLE_URL = Item.prepare_url('adservices/%(id)s/kind/%(kind)s')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """

        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)

    def getOne(self, _id, **kwargs):
        """
        Args:
            _id (int)

        """
        data = {
            'url': self.SINGLE_URL,
            'id': Item.sanitize_id(_id),
        }

        return self.transport.get().request(**data)

    def getForKind(self, kind=None, **kwargs):
        """
        Args:
            kind (str)
            limit (int)
            offset (int)

        """
        request_data = {
            'url': self.KIND_URL,
            'kind': self.sanitize_non_blank_value(kind, 'kind'),
        }

        return self.transport.get().set_pagination(**kwargs).request(**request_data)

    def getForKindOne(self, _id, kind, **kwargs):
        """
        Args:
            _id (int)
            kind (str)

        """
        request_data = {
            'url': self.KIND_SINGLE_URL,
            'id': self.sanitize_id(_id),
            'kind': self.sanitize_non_blank_value(kind, 'kind'),
        }

        return self.transport.get().request(**request_data)


class CampaignCategories(Item):
    """
    List of campaigns categories

    """

    SCOPE = 'public_data'

    ORDERING = ('name',)

    URL = Item.prepare_url('categories')
    SINGLE_URL = Item.prepare_url('categories/%(id)s')

    def get(self, **kwargs):
        """
        Args:
            campaign (list of int)
            language (str)
            order_by (str)
            limit (int)
            offset (int)

        """
        ordering = {
            'order_by': kwargs.get('order_by', None),
            'available': self.ORDERING
        }

        filtering = {
            'filter_by': kwargs,
            'available': {
                'campaign': lambda x: Item.sanitize_integer_array(x, 'campaign', True),
                'language': lambda x: Item.sanitize_string_value(x, 'language', 2, 2, True),
            }
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_ordering(ordering) \
                   .set_filtering(filtering) \
                   .request(url=self.URL)

    def getOne(self, _id, **kwargs):
        """
        Args:
            _id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'id': Item.sanitize_id(_id)
        }

        return self.transport.get().request(**request_data)

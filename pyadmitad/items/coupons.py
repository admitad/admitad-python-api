# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Coupons',
    'CouponsForWebsite',
    'CouponsCategories',
]


class CouponsBase(Item):

    ORDERING = ('name', 'date_start', 'date_end', 'rating',)
    FILTERING = {
        'campaign': lambda x: Item.sanitize_integer_array(x, 'campaign', blank=True),
        'campaign_category': lambda x: Item.sanitize_integer_array(x, 'campaign_category', blank=True),
        'category': lambda x: Item.sanitize_integer_array(x, 'category', blank=True),
        'type': lambda x: Item.sanitize_string_value(x, 'type', blank=True),
    }


class Coupons(CouponsBase):
    """
    List of coupons

    """

    SCOPE = 'coupons'

    URL = Item.prepare_url('coupons')
    SINGLE_URL = Item.prepare_url('coupons/%(coupon_id)s')

    def get(self, **kwargs):
        """
        Args:
            campaign (list of int)
            campaign_category (list of int)
            category (list of int)
            type (str)
            limit (int)
            offset (int)
            order_by (str)

        """
        filtering = {
            'filter_by': kwargs,
            'available': self.FILTERING
        }

        ordering = {
            'order_by': kwargs.get('order_by', None),
            'available': self.ORDERING
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
            'coupon_id': Item.sanitize_id(_id)
        }

        return self.transport.get().request(**request_data)


class CouponsForWebsite(CouponsBase):
    """
    List of the website coupons

    """

    SCOPE = 'coupons_for_website'

    URL = Item.prepare_url('coupons/website/%(website_id)s')
    SINGLE_URL = Item.prepare_url('coupons/%(campaign_id)s/website/%(website_id)s')

    def get(self, _id, **kwargs):
        """
        Here _id is a websites id

        Args:
            _id (int)
            campaign (list of int)
            campaign_category (list of int)
            category (list of int)
            type (str)
            limit (int)
            offset (int)
            order_by (str)

        """
        request_data = {
            'url': self.URL,
            'website_id': Item.sanitize_id(_id)
        }

        filtering = {
            'filter_by': kwargs,
            'available': self.FILTERING
        }

        ordering = {
            'order_by': kwargs.get('order_by', None),
            'available': self.ORDERING
        }

        return self.transport.get() \
                   .set_pagination(**kwargs) \
                   .set_ordering(ordering) \
                   .set_filtering(filtering) \
                   .request(**request_data)

    def getOne(self, _id, c_id, **kwargs):
        """
        Here _id is a websites id and c_id is a coupon id

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


class CouponsCategories(CouponsBase):

    SCOPE = 'public_data'

    URL = Item.prepare_url('coupons/categories')
    SINGLE_URL = Item.prepare_url('coupons/categories/%(coupon_category_id)s')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """
        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)

    def getOne(self, coupon_category_id):
        """
        Args:
            coupon_category_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'coupon_category_id': Item.sanitize_id(coupon_category_id)
        }

        return self.transport.get().request(**request_data)

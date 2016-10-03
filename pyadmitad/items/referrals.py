# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'Referrals',
]


class Referrals(Item):
    """
    List of referrals

    """

    SCOPE = 'referrals'

    URL = Item.prepare_url('referrals')
    SINGLE_URL = Item.prepare_url('referrals/%(referral_id)s')

    def get(self, **kwargs):
        """
        Args:
            date_start (date)
            date_end (date)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'date_start': lambda x: Item.sanitize_date(x, 'date_start', True),
                'date_end': lambda x: Item.sanitize_date(x, 'date_end', True)
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
        request_data = {
            'url': self.SINGLE_URL,
            'referral_id': Item.sanitize_id(_id)
        }

        return self.transport.get().request(**request_data)

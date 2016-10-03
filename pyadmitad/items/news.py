# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = [
    'News',
]


class News(Item):
    """
    List of news

    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('news')
    SINGLE_URL = Item.prepare_url('news/%(news_id)s')

    def get(self, **kwargs):
        """
        Args:
            limit (int)
            offset (int)

        """
        return self.transport.get().set_pagination(**kwargs).request(url=self.URL)

    def getOne(self, news_id):
        """
        Args:
            news_id (int)

        """
        data = {
            'url': self.SINGLE_URL,
            'news_id': self.sanitize_id(news_id)
        }

        return self.transport.get().request(**data)

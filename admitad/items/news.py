from admitad.items.base import Item


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
            language (str)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'language': lambda x: Item.sanitize_string_value(x, 'language', 2, 2, True),
            }
        }

        return self.transport.get() \
            .set_pagination(**kwargs) \
            .set_filtering(filtering) \
            .request(url=self.URL)

    def getOne(self, news_id, **kwargs):
        """
        Args:
            news_id (int)
            language (str)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'news_id': self.sanitize_id(news_id)
        }

        filtering = {
            'filter_by': kwargs,
            'available': {
                'language': lambda x: Item.sanitize_string_value(x, 'language', 2, 2, True),
            }
        }

        return self.transport.get().set_filtering(filtering).request(**request_data)

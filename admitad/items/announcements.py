from admitad.items.base import Item


__all__ = [
    'Announcements',
]


class Announcements(Item):
    """
    List of announcements

    """

    SCOPE = 'announcements'

    URL = Item.prepare_url('announcements')
    SINGLE_URL = Item.prepare_url('announcements/%(announcement_id)s')

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

    def getOne(self, _id, **kwargs):
        """
        Args:
            _id (int)
            language (str)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'language': lambda x: Item.sanitize_string_value(x, 'language', 2, 2, True),
            }
        }

        request_data = {
            'url': self.SINGLE_URL,
            'announcement_id': Item.sanitize_id(_id)
        }

        return self.transport.get().set_filtering(filtering).request(**request_data)

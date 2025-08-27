from admitad.items.base import Item


__all__ = [
    'LostOrders',
    'LostOrdersManager',
]


class LostOrders(Item):

    SCOPE = 'lost_orders'

    URL = Item.prepare_url('lost_orders')
    SINGLE_URL = Item.prepare_url('lost_orders/%(lost_order_id)s')

    def get(self, **kwargs):
        """
        Args:
            campaign (id)
            website (id)
            status (string)
            start_date (date)
            end_date (date)
            appeal_id (string)
            appeal_status (string)
            limit (int)
            offset (int)

        """
        filtering = {
            'filter_by': kwargs,
            'available': {
                'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign', blank=True),
                'website': lambda x: Item.sanitize_integer_value(x, 'website', blank=True),
                'status': lambda x: Item.sanitize_string_value(x, 'status', blank=True),
                'start_date': lambda x: Item.sanitize_string_value(x, 'start_date', blank=True),
                'end_date': lambda x: Item.sanitize_string_value(x, 'end_date', blank=True),
                'appeal_id': lambda x: Item.sanitize_string_value(x, 'appeal_id', blank=True),
                'appeal_status': lambda x: Item.sanitize_string_value(x, 'appeal_status', blank=True),
            }
        }

        return self.transport.get() \
            .set_filtering(filtering) \
            .set_pagination(**kwargs) \
            .request(url=self.URL)

    def getOne(self, lost_order_id):
        """
        Args:
            lost_order_id (int)

        """
        request_data = {
            'url': self.SINGLE_URL,
            'lost_order_id': Item.sanitize_id(lost_order_id)
        }

        return self.transport.get().request(**request_data)


class LostOrdersManager(Item):

    SCOPE = 'manage_lost_orders'

    DELETE_URL = Item.prepare_url('lost_orders/%(lost_order_id)s/decline')
    CREATE_URL = Item.prepare_url('lost_orders/create')
    UPDATE_URL = Item.prepare_url('lost_orders/%(lost_order_id)s/update')

    CREATE_FIELDS = {
        'campaign': lambda x: Item.sanitize_integer_value(x, 'campaign'),
        'website': lambda x: Item.sanitize_integer_value(x, 'website'),
        'order_id': lambda x: Item.sanitize_string_value(x, 'order_id'),
        'order_date': lambda x: Item.sanitize_date(x, 'order_date'),
        'order_price': lambda x: Item.sanitize_float_value(x, 'order_price'),
        'comment': lambda x: Item.sanitize_string_value(x, 'comment'),
        'appeal_id': lambda x: Item.sanitize_string_value(x, 'appeal_id'),
    }

    def delete(self, lost_order_id):
        """
        Args:
            lost_order_id (int)

        """
        request_data = {
            'url': self.DELETE_URL,
            'lost_order_id': Item.sanitize_id(lost_order_id),
        }

        return self.transport.delete().request(**request_data)

    def create(self, attachments, **kwargs):
        """
        Args:
            attachments (list of str)
            campaign (int)
            website (int)
            order_id (str)
            order_date (date)
            order_price (float)
            appeal_id (str)
            comment (str)

        """
        data = Item.sanitize_fields(self.CREATE_FIELDS, **kwargs)
        files = [('attachment', open(item, 'rb')) for item in Item.sanitize_string_array(attachments, 'attachments')]

        return self.transport.post().set_data(data).set_files(files).request(url=self.CREATE_URL)

    def update(self, lost_order_id, appeal_status):
        """
        Args:
            lost_order_id (int)
            appeal_status (str)

        """
        request_data = {
            'url': self.UPDATE_URL,
            'lost_order_id': Item.sanitize_id(lost_order_id),
        }

        data = {
            'appeal_status': self.sanitize_string_value(appeal_status, 'appeal_status'),
        }

        return self.transport.put().set_data(data).request(**request_data)

# coding: utf-8
from __future__ import unicode_literals

from pyadmitad.items.base import Item


__all__ = (
    'Me',
    'Balance',
    'PaymentsSettings',
)


class Me(Item):
    """
    Get private information

    """

    SCOPE = 'private_data private_data_email private_data_phone'

    URL = Item.prepare_url('me')

    def __call__(self):
        return self.get()

    def get(self):
        return self.transport.get().request(url=self.URL)


class Balance(Item):
    """
    Get balance information

    """

    SCOPE = 'private_data_balance'

    URL = Item.prepare_url('me/balance')
    EXTENDED_URL = Item.prepare_url('me/balance/extended')

    def __call__(self, **kwargs):
        return self.get(**kwargs)

    def get(self, **kwargs):
        """
        Args:
            extended (bool)

        """
        url = self.EXTENDED_URL if kwargs.get('extended', False) else self.URL

        return self.transport.get().request(url=url)


class PaymentsSettings(Item):
    """
    Get payments settings by currency

    """

    SCOPE = 'private_data_balance'

    URL = Item.prepare_url('me/payment/settings')
    CURRENCY_URL = Item.prepare_url('me/payment/settings/%(currency)s')

    def __call__(self, **kwargs):
        return self.get(**kwargs)

    def get(self, currency=None):
        """
        Args:
            currency (str)

        """
        request_data = {
            'currency': Item.sanitize_currency_value(currency, blank=True),
            'url': self.CURRENCY_URL if currency else self.URL
        }

        return self.transport.get().request(**request_data)

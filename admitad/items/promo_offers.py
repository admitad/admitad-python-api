from admitad.items.base import Item


class PromoOffersForCampaign(Item):
    """
    List of the campaign promo offers
    """

    SCOPE = 'public_data'

    URL = Item.prepare_url('promo_offers/%(campaign_id)s')

    def get(self, _id: int, **kwargs: dict) -> dict:
        """
        Args:
            _id (int): campaign id
            limit (int): limit of the response
            offset (int): offset of the response
        """

        request_data = {
            'url': self.URL,
            'campaign_id': Item.sanitize_id(_id)
        }

        return (
            self.transport.get()
            .set_pagination(**kwargs)
            .request(**request_data)
        )

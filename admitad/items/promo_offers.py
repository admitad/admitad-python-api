from admitad.items.base import Item


__all__ = [
    'PromoOffersForCampaign',
    'PromoOfferRequestTrackingCode',
]


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


class PromoOfferRequestTrackingCode(Item):
    """
    Request tracking promo code for website from specific promo offer
    """

    SCOPE = 'request_tracking_coupon'

    URL = Item.prepare_url('advcampaigns/request-tracking-coupon')

    def request(
        self,
        coupon_id: int,
        advcampaign_id: int,
        website_id: int,
    ) -> dict:
        """
        Args:
            coupon_id (int): ID promo offer (coupon)
            advcampaign_id (int): ID advertising campaign
            website_id (int): ID website

        Returns:
            dict: Answer with assigned promo code and tracking link
                {
                    "assigned_promo_code": str | None,  # promo code or None if request is created
                    "tracking_link": str | None,        # tracking link or None
                }
        """
        request_data = {
            'coupon_id': Item.sanitize_id(coupon_id),
            'advcampaign_id': Item.sanitize_id(advcampaign_id),
            'website_id': Item.sanitize_id(website_id),
        }

        return (
            self.transport.post()
            .set_data(request_data)
            .request(url=self.URL)
        )

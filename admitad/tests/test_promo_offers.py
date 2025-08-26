import unittest
import responses

from admitad.items import PromoOffersForCampaign
from admitad.tests.base import BaseTestCase


class PromoOffersForCampaignTestCase(BaseTestCase):

    def test_get_promo_offers_for_campaign_request(self):
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                self.prepare_url(PromoOffersForCampaign.URL, campaign_id=12, params={
                    'limit': 10,
                    'offset': 0
                }),
                match_querystring=True,
                json={'status': 'ok'},
                status=200
            )
            result = self.client.PromoOffersForCampaign.get(12, limit=10, offset=0)

        self.assertIn('status', result)


if __name__ == '__main__':
    unittest.main()

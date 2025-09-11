import unittest
import responses

from admitad.exceptions import HttpException
from admitad.items import PromoOffersForCampaign, PromoOfferRequestTrackingCode
from admitad.tests.base import BaseTestCase


class PromoOffersForCampaignTestCase(BaseTestCase):

    def test_get_promo_offers_for_campaign_request(self) -> None:
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


class PromoOfferRequestTrackingCodeTestCase(BaseTestCase):

    def test_request_tracking_promo_code_success(self) -> None:
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                PromoOfferRequestTrackingCode.CREATE_URL,
                json={
                    'assigned_promo_code': 'TESTCODE123',
                    'tracking_link': 'https://ad.admitad.com/g/123abc/'
                },
                status=200
            )
            result = self.client.PromoOfferRequestTrackingCode.create(
                coupon_id=100,
                advcampaign_id=200,
                website_id=300
            )

        self.assertIn('assigned_promo_code', result)
        self.assertIn('tracking_link', result)
        self.assertEqual(result['assigned_promo_code'], 'TESTCODE123')

    def test_request_tracking_promo_code_creates_request(self) -> None:
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                PromoOfferRequestTrackingCode.CREATE_URL,
                json={
                    'assigned_promo_code': None,
                    'tracking_link': None,
                    'request_id': 123,
                },
                status=200
            )
            result = self.client.PromoOfferRequestTrackingCode.create(
                coupon_id=100,
                advcampaign_id=200,
                website_id=300
            )

        self.assertIn('assigned_promo_code', result)
        self.assertIn('tracking_link', result)
        self.assertIsNone(result['assigned_promo_code'])
        self.assertIsNone(result['tracking_link'])
        self.assertEqual(result['request_id'], 123)

    def test_request_tracking_promo_code_no_coupon_error(self) -> None:
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                PromoOfferRequestTrackingCode.CREATE_URL,
                json={
                    'error_code': 'CHECK_PRE_APPROVED_COUPON_ERROR_CODE_NO_COUPON'
                },
                status=400
            )
            with self.assertRaises(HttpException):
                self.client.PromoOfferRequestTrackingCode.create(
                    coupon_id=100,
                    advcampaign_id=200,
                    website_id=300
                )

    def test_request_tracking_promo_code_not_connected_error(self) -> None:
        with responses.RequestsMock() as resp:
            resp.add(
                resp.POST,
                PromoOfferRequestTrackingCode.CREATE_URL,
                json={
                    'error_code': 'webmaster_not_connected'
                },
                status=400
            )
            with self.assertRaises(HttpException):
                self.client.PromoOfferRequestTrackingCode.create(
                    coupon_id=100,
                    advcampaign_id=200,
                    website_id=300
                )

    def test_request_tracking_promo_code_invalid_coupon_id(self) -> None:
        with self.assertRaises(ValueError):
            self.client.PromoOfferRequestTrackingCode.create(
                coupon_id=0,  # Invalid ID
                advcampaign_id=200,
                website_id=300
            )

    def test_request_tracking_promo_code_invalid_advcampaign_id(self) -> None:
        with self.assertRaises(ValueError):
            self.client.PromoOfferRequestTrackingCode.create(
                coupon_id=100,
                advcampaign_id=0,
                website_id=300
            )

    def test_request_tracking_promo_code_invalid_website_id(self) -> None:
        with self.assertRaises(ValueError):
            self.client.PromoOfferRequestTrackingCode.create(
                coupon_id=100,
                advcampaign_id=200,
                website_id=0,
            )

    def test_get_tracking_promo_code_request_status_success(self) -> None:
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                PromoOfferRequestTrackingCode.GET_STATUS_URL,
                json={
                    "request_id": 8,
                    "promo_offer_id": 100,
                    "website_id": 300,
                    "status": "approved",
                    "approved_at": "2023-01-01T12:00:00Z",
                    "declined_at": None,
                    "created_at": "2023-01-01T10:00:00Z",
                    "assigned_promo_code": "TESTCODE123"
                },
                status=200
            )
            result = self.client.PromoOfferRequestTrackingCode.get(request_id=8)

        self.assertIn('request_id', result)
        self.assertIn('status', result)
        self.assertEqual(result['request_id'], 8)
        self.assertEqual(result['status'], 'approved')
        self.assertEqual(result['assigned_promo_code'], 'TESTCODE123')

    def test_get_tracking_promo_code_request_status_not_found(self) -> None:
        with responses.RequestsMock() as resp:
            resp.add(
                resp.GET,
                PromoOfferRequestTrackingCode.GET_STATUS_URL,
                json={"err_code": "PROMO_REQUEST_NOT_FOUND"},
                status=404
            )
            with self.assertRaises(HttpException):
                self.client.PromoOfferRequestTrackingCode.get(request_id=999)

    def test_get_tracking_promo_code_request_invalid_id(self) -> None:
        with self.assertRaises(ValueError):
            self.client.PromoOfferRequestTrackingCode.get(request_id=0)


if __name__ == '__main__':
    unittest.main()

# coding: utf-8
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()

from unittest import TestCase
from urllib.parse import urlencode

from pyadmitad.api import get_oauth_client_token


class BaseTestCase(TestCase):
    client = get_oauth_client_token(access_token='')

    @staticmethod
    def prepare_url(url, params=None, **kwargs):
        base = url % kwargs

        return base if not params else '%s?%s' % (base, urlencode(params, doseq=True))

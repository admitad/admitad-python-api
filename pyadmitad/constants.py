# coding: utf-8
from __future__ import unicode_literals

# API date-format
DATE_FORMAT = '%d.%m.%Y'
LONG_DATE_FORMAT = '%d.%m.%Y %H:%M:%S'

SUPPORTED_LANGUAGES = ('ru', 'en', 'de', 'pl', 'es', 'tr')

# default values
DEFAULT_REQUEST_TIMEOUT = 60
DEFAULT_LANGUAGE = 'ru'
DEFAULT_PAGINATION_LIMIT = 20
DEFAULT_PAGINATION_OFFSET = 0

# constants
MAX_PAGINATION_LIMIT = 500
MAX_SUB_ID_LENGTH = 250

# urls
BASE_URL = 'https://api.admitad.com/'
AUTHORIZE_URL = '%s%s' % (BASE_URL, 'authorize/')
TOKEN_URL = '%s%s' % (BASE_URL, 'token/')

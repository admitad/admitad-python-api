import os

DATE_FORMAT: str = '%d.%m.%Y'
LONG_DATE_FORMAT: str = '%d.%m.%Y %H:%M:%S'

SUPPORTED_LANGUAGES: tuple[str, ...] = ('ru', 'en', 'de', 'pl', 'es', 'tr')

DEFAULT_REQUEST_TIMEOUT: int = 60
DEFAULT_LANGUAGE: str = 'ru'
DEFAULT_PAGINATION_LIMIT: int = 20
DEFAULT_PAGINATION_OFFSET: int = 0

MAX_PAGINATION_LIMIT: int = 500
MAX_SUB_ID_LENGTH: int = 250

DEFAULT_PROD_URL: str = 'https://api.admitad.com/'
CUSTOM_BASE_URL: str = os.getenv('ADMITAD_API_LIB_BASE_URL')

BASE_URL: str = (CUSTOM_BASE_URL or DEFAULT_PROD_URL).rstrip('/') + '/'
AUTHORIZE_URL: str = f'{BASE_URL}authorize/'
TOKEN_URL: str = f'{BASE_URL}token/'

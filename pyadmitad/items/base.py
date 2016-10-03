# coding: utf-8
from __future__ import unicode_literals

from future import standard_library
standard_library.install_aliases()

from future.builtins import int, str
from datetime import datetime, date
from urllib.parse import urljoin

from pyadmitad.constants import BASE_URL, DATE_FORMAT, LONG_DATE_FORMAT


class Item(object):

    def __init__(self, transport):
        self.transport = transport
        self.transport.clean_data()

    @staticmethod
    def sanitize_fields(fields, **kwargs):
        return {key: func(kwargs.get(key, None)) for (key, func) in fields.items()}

    @staticmethod
    def sanitize_id(_id, name='_id'):
        if _id == 0:
            raise ValueError('Invalid value for `id`: %s' % (_id))
        return Item.sanitize_integer_value(_id, name, False)

    @staticmethod
    def sanitize_non_blank_value(value, name):
        if value in [[], {}, (), '', None]:
            raise ValueError("Invalid non-blank value '%s': %s" % (name, value))
        return value

    @staticmethod
    def sanitize_string_value(value, name, max_length=None, min_length=None, blank=False):
        if not value:
            if not blank:
                raise ValueError("Invalid string value '%s': %s. Cannot be blank." %
                                 (name, value))
            return value
        if max_length and len(value) > max_length:
            raise ValueError("Invalid string value '%s': %s. Max length: %s" %
                             (name, value, max_length))
        if min_length and len(value) < min_length:
            raise ValueError("Invalid string value '%s': %s. Min length: %s" %
                             (name, value, min_length))
        return value

    @staticmethod
    def sanitize_integer_value(value, name, blank=False):
        if value is None:
            if not blank:
                raise ValueError("Blank integer value '%s': %s" % (name, value))
            return value
        if isinstance(value, int):
            return value
        elif isinstance(value, str) and value.isdigit():
            return value
        raise ValueError("Invalid integer value '%s': %s" % (name, value))

    @staticmethod
    def sanitize_float_value(value, name, blank=False):
        if value is None:
            if not blank:
                raise ValueError("Blank float value '%s': %s" % (name, value))
            return value
        if isinstance(value, (float, int)):
            return value
        elif isinstance(value, str):
            try:
                float(value)
                return value
            except ValueError:
                pass
        raise ValueError("Invalid float value '%s': %s" % (name, value))

    @staticmethod
    def sanitize_integer_array(values, name, blank=False):
        if not values:
            if not blank:
                raise ValueError("Blank integer values '%s': %s" % (name, values))
            return values
        if not isinstance(values, (list, tuple, set)):
            values = [values]
        return [Item.sanitize_integer_value(x, name, blank=blank)
                for x in values]

    @staticmethod
    def sanitize_string_array(values, name, max_length=None, min_length=None, blank=False):
        if not values:
            if not blank:
                raise ValueError("Blank string values '%s': %s" % (name, values))
            return values
        if not isinstance(values, (list, tuple, set)):
            values = [values]
        return [Item.sanitize_string_value(x, name, max_length=max_length, min_length=min_length, blank=blank)
                for x in values]

    @staticmethod
    def sanitize_bool_value(value, name='', blank=False):
        if value is None:
            if not blank:
                raise ValueError("Blank bool value '%s': %s" % (name, value))
            return False
        return str(bool(value)).lower()

    @staticmethod
    def sanitize_bool_integer_value(value, name='', blank=False):
        if value is None:
            if not blank:
                raise ValueError("Blank bool value '%s': %s" % (name, value))
            return False
        return 1 if value else 0

    @staticmethod
    def sanitize_currency_value(value, blank=True):
        if not value:
            if not blank:
                raise ValueError("Blank currency value: %s" % value)
            return value
        if not len(value) == 3:
            raise ValueError("Invalid currency value: %s" % value)
        return value.upper()

    @staticmethod
    def sanitize_date(value, name, blank=False):
        if value is None:
            if not blank:
                raise ValueError("Blank date value for '%s'" % name)
            return None
        if isinstance(value, datetime):
            return value.date().strftime(DATE_FORMAT)
        elif isinstance(value, date):
            return value.strftime(DATE_FORMAT)
        elif isinstance(value, str):
            try:
                datetime.strptime(value, DATE_FORMAT)
            except ValueError:
                raise ValueError("Invalid date: %s" % value)
            return value
        raise ValueError("Invalid date: %s" % value)

    @staticmethod
    def sanitize_long_date(value, name, blank=False):
        if value is None:
            if not blank:
                raise ValueError("Blank date value for '%s'" % name)
            return None
        if isinstance(value, datetime):
            return value.strftime(LONG_DATE_FORMAT)
        elif isinstance(value, str):
            try:
                datetime.strptime(value, LONG_DATE_FORMAT)
            except ValueError:
                raise ValueError("Invalid date: %s" % value)
            return value
        raise ValueError("Invalid date: %s" % value)

    @staticmethod
    def prepare_url(path):
        url = urljoin(BASE_URL, path)
        if not url.endswith('/'):
            url += '/'
        return url

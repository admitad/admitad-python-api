# coding: utf-8
from __future__ import unicode_literals

import unittest
from datetime import datetime, date

from pyadmitad.items.base import Item
from pyadmitad.tests.base import BaseTestCase
from pyadmitad.constants import BASE_URL


class ItemTestCase(BaseTestCase):

    def test_sanitize_id(self):
        self.assertEqual(Item.sanitize_id(2, ''), 2)
        self.assertEqual(Item.sanitize_id(2**64, ''), 2**64)
        self.assertEqual(Item.sanitize_id('64', ''), '64')

        with self.assertRaises(ValueError):
            Item.sanitize_id(0, '')
            Item.sanitize_id(None, '')
            Item.sanitize_id(3.14, '')
            Item.sanitize_id('foo', '')

    def test_sanitize_fields(self):
        fields = {
            'field1': lambda x: Item.sanitize_non_blank_value(x, ''),
            'field2': lambda x: Item.sanitize_integer_value(x, ''),
            'field3': lambda x: Item.sanitize_string_value(x, '', blank=True),
        }

        data = Item.sanitize_fields(fields, field1='foobarbaz', field2=42, field3='')

        self.assertDictEqual(data, {
            'field1': 'foobarbaz',
            'field2': 42,
            'field3': ''
        })

        data = Item.sanitize_fields(fields, field1='foobarbaz', field2=42, field3='', field4='another')

        self.assertDictEqual(data, {
            'field1': 'foobarbaz',
            'field2': 42,
            'field3': ''
        })

    def test_sanitize_non_blank_value(self):
        self.assertEqual(Item.sanitize_non_blank_value(0, ''), 0)
        self.assertEqual(Item.sanitize_non_blank_value('a', ''), 'a')
        self.assertListEqual(Item.sanitize_non_blank_value([1], ''), [1])
        self.assertDictEqual(Item.sanitize_non_blank_value({'a': 1}, ''), {'a': 1})
        self.assertTupleEqual(Item.sanitize_non_blank_value((1, 2), ''), (1, 2))

        with self.assertRaises(ValueError):
            Item.sanitize_non_blank_value('', '')
            Item.sanitize_non_blank_value([], '')
            Item.sanitize_non_blank_value({}, '')
            Item.sanitize_non_blank_value((), '')
            Item.sanitize_non_blank_value(None, '')

    def test_sanitize_string_value(self):
        self.assertEqual(Item.sanitize_string_value('foo', '', 10, None, False), 'foo')
        self.assertEqual(Item.sanitize_string_value('foo', '', None, 2, False), 'foo')
        self.assertEqual(Item.sanitize_string_value('foobarbaz', '', 10, 5, False), 'foobarbaz')
        self.assertEqual(Item.sanitize_string_value('', '', None, None, True), '')

        with self.assertRaises(ValueError):
            Item.sanitize_string_value('', '', None, None, False)
            Item.sanitize_string_value('foo', '', 2, None, False)
            Item.sanitize_string_value('foo', '', None, 5, False)
            Item.sanitize_string_value('foobarbaz', '', 5, 6, False)

    def test_sanitize_integer_value(self):
        self.assertEqual(Item.sanitize_integer_value(2, '', False), 2)
        self.assertEqual(Item.sanitize_integer_value(0, '', False), 0)
        self.assertEqual(Item.sanitize_integer_value(None, '', True), None)
        self.assertEqual(Item.sanitize_integer_value(2**64, '', False), 2**64)
        self.assertEqual(Item.sanitize_integer_value('64', '', False), '64')

        with self.assertRaises(ValueError):
            Item.sanitize_integer_value(None, '', False)
            Item.sanitize_integer_value(3.14, '', False)
            Item.sanitize_integer_value('foo', '', False)

    def test_sanitize_float_value(self):
        self.assertEqual(Item.sanitize_float_value(1, '', False), 1)
        self.assertEqual(Item.sanitize_float_value(0, '', False), 0)
        self.assertEqual(Item.sanitize_float_value('12', '', False), '12')
        self.assertEqual(Item.sanitize_float_value('3.14', '', False), '3.14')
        self.assertEqual(Item.sanitize_float_value(3.14, '', False), 3.14)
        self.assertEqual(Item.sanitize_float_value(None, '', True), None)

        with self.assertRaises(ValueError):
            Item.sanitize_float_value(None, '', False)
            Item.sanitize_float_value('foo', '', False)

    def test_sanitize_integer_array(self):
        self.assertEqual(Item.sanitize_integer_array(None, '', True), None)
        self.assertEqual(Item.sanitize_integer_array([], '', True), [])
        self.assertListEqual(Item.sanitize_integer_array([0, 1, '12'], '', False), [0, 1, '12'])
        self.assertListEqual(Item.sanitize_integer_array([5, None, '1', None], '', True), [5, None, '1', None])
        self.assertListEqual(Item.sanitize_integer_array(5, ''), [5])

        with self.assertRaises(ValueError):
            Item.sanitize_integer_array(None, '', False)
            Item.sanitize_integer_array([], '', False)
            Item.sanitize_integer_array([1, 2, 3, None, 5], '', False)

    def test_sanitize_string_array(self):
        self.assertEqual(Item.sanitize_string_array(None, '', None, None, True), None)
        self.assertListEqual(Item.sanitize_string_array([], '', None, None, True), [])
        self.assertListEqual(Item.sanitize_string_array('foo', ''), ['foo'])
        self.assertListEqual(Item.sanitize_string_array([''], '', None, None, True), [''])
        self.assertListEqual(Item.sanitize_string_array(['foo', 'bar'], '', 10, 2, False), ['foo', 'bar'])
        self.assertListEqual(Item.sanitize_string_array(['foo', 'bar'], '', None, None, False), ['foo', 'bar'])

        with self.assertRaises(ValueError):
            Item.sanitize_string_array(None, '', False)
            Item.sanitize_string_array([], '', False)
            Item.sanitize_string_array([''], '', False)
            Item.sanitize_string_array(['foobarbaz'], '', 5, 3, False)
            Item.sanitize_string_array(['foobarbaz'], '', 5, None, False)
            Item.sanitize_string_array(['foo'], '', None, 5, False)

    def test_sanitize_currency(self):
        self.assertEqual(Item.sanitize_currency_value(None, True), None)
        self.assertEqual(Item.sanitize_currency_value('', True), '')
        self.assertEqual(Item.sanitize_currency_value('usd', False), 'USD')
        self.assertEqual(Item.sanitize_currency_value('EUR', False), 'EUR')

        with self.assertRaises(ValueError):
            Item.sanitize_currency_value(None, False)
            Item.sanitize_currency_value('', False)
            Item.sanitize_currency_value('foobarbaz', True)
            Item.sanitize_currency_value('12', True)

    def test_sanitize_date(self):
        self.assertEqual(Item.sanitize_date(None, '', True), None)
        self.assertEqual(Item.sanitize_date(datetime(2020, 1, 1), '', False), '01.01.2020')
        self.assertEqual(Item.sanitize_date(date(2020, 1, 1), '', False), '01.01.2020')
        self.assertEqual(Item.sanitize_date('01.01.2020', '', False), '01.01.2020')

        with self.assertRaises(ValueError):
            Item.sanitize_date(None, '', False)
            Item.sanitize_date('01/01/2020', '', True)

    def test_sanitize_long_date(self):
        self.assertEqual(Item.sanitize_long_date(None, '', True), None)
        self.assertEqual(Item.sanitize_long_date(datetime(2020, 1, 1, 11, 20, 36), '', False), '01.01.2020 11:20:36')
        self.assertEqual(Item.sanitize_long_date('01.01.2020 11:20:36', '', False), '01.01.2020 11:20:36')

        with self.assertRaises(ValueError):
            Item.sanitize_long_date(None, '', False)
            Item.sanitize_long_date('01/01/2020', '', True)
            Item.sanitize_long_date('01.01.2020 11/22/22', '', False)

    def test_prepare_url(self):
        self.assertEqual(Item.prepare_url('somepath'), '%ssomepath/' % BASE_URL)
        self.assertEqual(Item.prepare_url('somepath/'), '%ssomepath/' % BASE_URL)
        self.assertEqual(Item.prepare_url('/somepath'), '%ssomepath/' % BASE_URL)
        self.assertEqual(Item.prepare_url('/somepath/'), '%ssomepath/' % BASE_URL)


if __name__ == '__main__':
    unittest.main()

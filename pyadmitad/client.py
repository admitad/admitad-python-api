# coding: utf-8
from __future__ import unicode_literals

from pyadmitad import items


class Client(object):
    """The API client."""

    def __init__(self, transport):
        self.transport = transport

    def __getattr__(self, name):
        return getattr(items, name)(self.transport)

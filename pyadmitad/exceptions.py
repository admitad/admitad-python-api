# coding: utf-8
from __future__ import unicode_literals


class HttpException(Exception):

    def __init__(self, status, message, content):
        super(HttpException, self).__init__()

        self.status = status
        self.message = message
        self.content = content

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "HttpException(%s): %s%s" % (
            self.status, self.content,
            "\n%s" % self.message if self.message else "")


class ConnectionException(Exception):

    def __init__(self, content):
        super(ConnectionException, self).__init__()

        self.content = content

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "ConnectionException: %s" % self.content


class JsonException(Exception):

    def __init__(self, content):
        super(JsonException, self).__init__()

        self.content = content

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "JsonException: %s" % self.content


class ApiException(Exception):

    def __init__(self, content):
        super(ApiException, self).__init__()

        self.content = content

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return "ApiException: %s" % self.content

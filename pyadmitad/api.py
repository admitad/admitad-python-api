# coding: utf-8
from __future__ import unicode_literals

from pyadmitad import client, transport


def get_oauth_client_token(access_token, user_agent=None, debug=False):
    """
    Creates a client using an access token.

    """
    http_transport = transport.HttpTransport(access_token, user_agent=user_agent, debug=debug)
    return client.Client(http_transport)


def get_oauth_client_client(client_id, client_secret, scopes, user_agent=None, debug=False):
    """
    Creates a client using a client_id and client_secret.

    """
    auth = transport.oauth_client_authorization({
        'client_id': client_id,
        'client_secret': client_secret,
        'scopes': scopes
    })
    return get_oauth_client_token(auth['access_token'], user_agent=user_agent, debug=debug)

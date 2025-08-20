from admitad import items, transport


class Client:
    """The API client."""

    def __init__(self, transport: transport.HttpTransport):
        self.transport = transport

    def __getattr__(self, name: str) -> type[items.Item]:
        return getattr(items, name)(self.transport)

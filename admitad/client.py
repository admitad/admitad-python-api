from dataclasses import dataclass

from admitad import items, transport


@dataclass
class Client:
    _transport: transport.HttpTransport

    def __getattr__(self, name: str) -> type[items.Item]:
        return getattr(items, name)(self._transport)

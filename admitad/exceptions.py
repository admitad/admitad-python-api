from dataclasses import dataclass


@dataclass
class HttpException(Exception):
    status: int
    message: str
    content: str

    def __str__(self) -> str:
        return f"HttpException({self.status}): {self.message}\n{self.content}"

@dataclass
class ConnectionException(Exception):
    content: str

    def __str__(self) -> str:
        return f"ConnectionException: {self.content}"


@dataclass
class JsonException(Exception):
    content: str

    def __str__(self) -> str:
        return f"JsonException: {self.content}"


@dataclass
class ApiException(Exception):
    content: str

    def __str__(self) -> str:
        return f"ApiException: {self.content}"

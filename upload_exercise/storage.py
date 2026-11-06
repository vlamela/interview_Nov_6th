"""A storage boundary with a deterministic fake; nothing is uploaded or signed."""

from typing import Literal, Protocol
from urllib.parse import quote

type Operation = Literal['upload', 'delete']


class StorageClient(Protocol):
    """The only storage operation needed by the URL service."""

    def create_url(self, object_path: str, operation: Operation) -> str: ...


class FakeStorageClient:
    """Record requested operations and return deliberately non-routable example URLs."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Operation]] = []

    def create_url(self, object_path: str, operation: Operation) -> str:
        self.calls.append((object_path, operation))
        encoded_path = quote(object_path, safe='/')
        return f'https://storage.example.invalid/{encoded_path}?operation={operation}'

"""Supplied Pydantic contracts; framework-specific changes are not required."""

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class FileRequest(BaseModel):
    """Shared input rules for upload and deletion; values are never normalized."""

    model_config = ConfigDict(frozen=True, extra='forbid')

    market: str = Field(min_length=1, max_length=32)
    filename: str = Field(min_length=1, max_length=255)

    @field_validator('market')
    @classmethod
    def validate_market(cls, value: str) -> str:
        if re.fullmatch(r'[A-Za-z0-9_-]+', value) is None:
            raise ValueError('market must contain only ASCII letters, digits, underscores, or hyphens')
        return value

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, value: str) -> str:
        if value != value.strip():
            raise ValueError('filename must not have leading or trailing whitespace')
        if re.fullmatch(r'[A-Za-z0-9_-][A-Za-z0-9._ -]*', value) is None:
            raise ValueError('filename must start with an ASCII letter, digit, underscore, or hyphen; no paths allowed')
        return value


class UploadRequest(FileRequest):
    """Input for creating a new upload URL."""


class QuotaUploadRequest(UploadRequest):
    """A new upload's declared size; this is not evidence of bytes stored."""

    size_bytes: int = Field(ge=0, strict=True)


class DeleteRequest(FileRequest):
    """Input for deleting an existing file, including safe legacy filenames."""


class UrlResponse(BaseModel):
    """URL and object identity returned by the fake service."""

    model_config = ConfigDict(frozen=True, extra='forbid')

    signed_url: str = Field(repr=False)
    object_path: str


class FileRecord(BaseModel):
    """A stored metadata record; legacy extensions remain valid."""

    model_config = ConfigDict(frozen=True, extra='forbid')

    id: int
    market: str
    filename: str
    size_bytes: int = Field(ge=0)
    status: Literal['active', 'deleted']


class MarketUsage(BaseModel):
    """Aggregated active-file usage for one market."""

    model_config = ConfigDict(frozen=True, extra='forbid')

    market: str
    file_count: int = Field(ge=0)
    total_bytes: int = Field(ge=0)


class ReservationRecord(BaseModel):
    """Capacity reserved by another workflow; expiry is an integer UTC Unix timestamp."""

    model_config = ConfigDict(frozen=True, extra='forbid')

    id: int
    market: str
    filename: str
    size_bytes: int = Field(ge=0)
    status: Literal['pending', 'completed', 'cancelled']
    expires_at: int = Field(ge=0)

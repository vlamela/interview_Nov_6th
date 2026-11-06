"""Working URL operations and a quota pilot to review before wider rollout."""

import sqlite3
from pathlib import PurePosixPath

from upload_exercise.models import DeleteRequest, QuotaUploadRequest, UploadRequest, UrlResponse
from upload_exercise.repository import get_market_usage
from upload_exercise.storage import StorageClient


class QuotaExceededError(ValueError):
    """The upload would exceed the market's supplied quota."""


def create_upload_url(request: UploadRequest, storage: StorageClient) -> UrlResponse:
    """Create a URL for a supported new-upload filename without normalizing it."""
    if PurePosixPath(request.filename).suffix.lower() not in {'.csv', '.xlsx'}:
        raise ValueError('filename must end in .csv or .xlsx')
    object_path = f'{request.market}/{request.filename}'
    signed_url = storage.create_url(object_path, 'upload')
    return UrlResponse(signed_url=signed_url, object_path=object_path)


def create_quota_checked_upload_url(
    request: QuotaUploadRequest,
    storage: StorageClient,
    connection: sqlite3.Connection,
    *,
    quota_bytes: int,
    now: int,
) -> UrlResponse:
    """Pilot quota check; review its accounting and guarantees against the brief."""
    if quota_bytes < 0:
        raise ValueError('quota_bytes must be non-negative')
    used_bytes = sum(usage.total_bytes for usage in get_market_usage(connection) if usage.market == request.market)
    if used_bytes + request.size_bytes > quota_bytes:
        raise QuotaExceededError('upload would exceed market quota')
    return create_upload_url(request, storage)


def create_delete_url(request: DeleteRequest, storage: StorageClient) -> UrlResponse:
    """Create a delete URL without imposing new-upload policies on legacy files."""
    object_path = f'{request.market}/{request.filename}'
    signed_url = storage.create_url(object_path, 'delete')
    return UrlResponse(signed_url=signed_url, object_path=object_path)

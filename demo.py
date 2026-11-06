"""Run one quota-check scenario without a test framework or external services."""

import argparse
from contextlib import closing

from upload_exercise.database import create_database
from upload_exercise.models import QuotaUploadRequest
from upload_exercise.service import QuotaExceededError, create_quota_checked_upload_url
from upload_exercise.storage import FakeStorageClient


def main() -> None:
    """Run a fresh synthetic request and print its decision and storage call count."""
    parser = argparse.ArgumentParser(description='Run one synthetic quota-check scenario.')
    parser.add_argument('--market', default='DE')
    parser.add_argument('--filename', default='new.csv')
    parser.add_argument('--size-bytes', type=int, default=200)
    parser.add_argument('--quota-bytes', type=int, default=500)
    parser.add_argument('--now', type=int, default=1000)
    arguments = parser.parse_args()
    request = QuotaUploadRequest(
        market=arguments.market,
        filename=arguments.filename,
        size_bytes=arguments.size_bytes,
    )
    storage = FakeStorageClient()

    with closing(create_database()) as connection:
        try:
            result = create_quota_checked_upload_url(
                request,
                storage,
                connection,
                quota_bytes=arguments.quota_bytes,
                now=arguments.now,
            )
        except QuotaExceededError as error:
            print(f'REJECTED: {error}')
        else:
            print(f'ACCEPTED: {result.object_path}')

    print(f'Storage calls: {len(storage.calls)}')


if __name__ == '__main__':
    main()

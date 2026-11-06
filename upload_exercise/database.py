"""Independent SQLite in-memory connections and synthetic file metadata."""

import sqlite3

from upload_exercise.models import FileRecord, ReservationRecord

_SCHEMA = """
CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    market TEXT NOT NULL,
    filename TEXT NOT NULL,
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    status TEXT NOT NULL CHECK (status IN ('active', 'deleted'))
);
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY,
    market TEXT NOT NULL,
    filename TEXT NOT NULL,
    size_bytes INTEGER NOT NULL CHECK (size_bytes >= 0),
    status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'cancelled')),
    expires_at INTEGER NOT NULL CHECK (expires_at >= 0)
);
"""

_SEED_FILES = (
    FileRecord(id=1, market='DE', filename='products.csv', size_bytes=120, status='active'),
    FileRecord(id=2, market='DE', filename='legacy.txt', size_bytes=80, status='active'),
    FileRecord(id=3, market='DE', filename='products.csv', size_bytes=30, status='active'),
    FileRecord(id=4, market='DE', filename='old.csv', size_bytes=999, status='deleted'),
    FileRecord(id=5, market='FR', filename='catalogue.xlsx', size_bytes=250, status='active'),
    FileRecord(id=6, market='FR', filename='empty.csv', size_bytes=0, status='active'),
    FileRecord(id=7, market='US', filename='removed.zip', size_bytes=500, status='deleted'),
)

_SEED_RESERVATIONS = (
    ReservationRecord(id=1, market='DE', filename='incoming.csv', size_bytes=100, status='pending', expires_at=2000),
    ReservationRecord(id=2, market='DE', filename='cancelled.csv', size_bytes=400, status='cancelled', expires_at=2000),
    ReservationRecord(id=3, market='DE', filename='finished.csv', size_bytes=600, status='completed', expires_at=2000),
    ReservationRecord(id=4, market='DE', filename='expired.csv', size_bytes=900, status='pending', expires_at=999),
    ReservationRecord(id=5, market='DE', filename='expires-now.csv', size_bytes=800, status='pending', expires_at=1000),
    ReservationRecord(id=6, market='FR', filename='incoming.xlsx', size_bytes=50, status='pending', expires_at=2000),
    ReservationRecord(id=7, market='GB', filename='incoming.csv', size_bytes=40, status='pending', expires_at=2000),
)


def create_database(*, seed: bool = True) -> sqlite3.Connection:
    """Return a new database; the caller owns and must close the connection."""
    connection = sqlite3.connect(':memory:')
    connection.row_factory = sqlite3.Row
    connection.executescript(_SCHEMA)
    if seed:
        with connection:
            connection.executemany(
                'INSERT INTO files (id, market, filename, size_bytes, status) VALUES (?, ?, ?, ?, ?)',
                [
                    (record.id, record.market, record.filename, record.size_bytes, record.status)
                    for record in _SEED_FILES
                ],
            )
            connection.executemany(
                'INSERT INTO reservations (id, market, filename, size_bytes, status, expires_at) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                [
                    (record.id, record.market, record.filename, record.size_bytes, record.status, record.expires_at)
                    for record in _SEED_RESERVATIONS
                ],
            )
    return connection

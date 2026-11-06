"""Working baseline metadata reads using SQL and Pydantic output models."""

import sqlite3

from upload_exercise.models import FileRecord, MarketUsage


def list_active_files(connection: sqlite3.Connection, market: str) -> list[FileRecord]:
    """Return this market's active files, ordered by filename then ID ascending."""
    rows = connection.execute(
        """
        SELECT id, market, filename, size_bytes, status
        FROM files
        WHERE market = ? AND status = 'active'
        ORDER BY filename ASC, id ASC
        """,
        (market,),
    ).fetchall()
    return [FileRecord.model_validate(dict(row)) for row in rows]


def get_market_usage(connection: sqlite3.Connection) -> list[MarketUsage]:
    """Aggregate active file counts and bytes per market, ordered by market ascending."""
    rows = connection.execute(
        """
        SELECT market, COUNT(*) AS file_count, SUM(size_bytes) AS total_bytes
        FROM files
        WHERE status = 'active'
        GROUP BY market
        ORDER BY market ASC
        """
    ).fetchall()
    return [MarketUsage.model_validate(dict(row)) for row in rows]

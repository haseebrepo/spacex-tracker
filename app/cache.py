import json
import os
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List

from app.settings import config


class ICache(ABC):
    """
    Interface for caching launch data.
    """

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def save(self, data: List[Dict[str, Any]]) -> None:
        raise NotImplementedError


class SQLiteCache(ICache):

    def __init__(
        self,
        table: str,
        db_path: str = config.DB_PATH,
        ttl_hours: int = config.CACHE_TTL_SECONDS,
    ):
        self.db_path = db_path
        self.table = table
        self.ttl = timedelta(hours=ttl_hours)
        self._ensure_table()

    def _ensure_table(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    timestamp DATETIME NOT NULL
                );
            """
            )

    def is_valid(self) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                f"SELECT timestamp FROM {self.table} ORDER BY timestamp DESC LIMIT 1;"
            )
            row = cur.fetchone()
            if not row:
                return False
            last_updated = datetime.fromisoformat(row[0])
            return datetime.utcnow() - last_updated < self.ttl

    def load(self) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(f"SELECT data FROM {self.table} ORDER BY id ASC;")
            return [json.loads(row[0]) for row in cur.fetchall()]

    def save(self, items: List[Dict[str, Any]]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"DELETE FROM {self.table};")
            now = datetime.utcnow().isoformat()
            for item in items:
                conn.execute(
                    f"INSERT INTO {self.table} (id, data, timestamp) VALUES (?, ?, ?);",
                    (item["id"], json.dumps(item), now),
                )

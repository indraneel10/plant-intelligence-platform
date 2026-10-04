import json
import sqlite3
from pathlib import Path


class EdgeObservationQueue:
    """Small durable SQLite queue for offline-first edge operation."""

    def __init__(self, path: str = "data/edge/queue.db") -> None:
        db_path = Path(path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(db_path)
        self.connection.execute("CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY AUTOINCREMENT, payload TEXT NOT NULL, sent INTEGER NOT NULL DEFAULT 0)")
        self.connection.commit()

    def enqueue(self, payload: dict) -> int:
        cursor = self.connection.execute("INSERT INTO queue(payload, sent) VALUES (?, 0)", (json.dumps(payload),))
        self.connection.commit()
        return int(cursor.lastrowid)

    def pending(self, limit: int = 100) -> list[tuple[int, dict]]:
        rows = self.connection.execute("SELECT id, payload FROM queue WHERE sent=0 ORDER BY id LIMIT ?", (limit,)).fetchall()
        return [(row[0], json.loads(row[1])) for row in rows]

    def mark_sent(self, item_id: int) -> None:
        self.connection.execute("UPDATE queue SET sent=1 WHERE id=?", (item_id,))
        self.connection.commit()

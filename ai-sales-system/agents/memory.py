"""
Shared Memory — Global Scratchpad for the LaunchMind Multi-Agent System.
Allows agents to store and retrieve shared facts and context.
Satisfies Assignment Requirement 4.1: "memory, scratchpads".
"""
import json
import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "agent_memory.db")

class SharedMemory:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                key        TEXT PRIMARY KEY,
                value      TEXT NOT NULL,
                agent_id   TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def store(self, key: str, value: any, agent_id: str):
        """Store a fact in shared memory."""
        val_str = json.dumps(value)
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("""
            INSERT OR REPLACE INTO memory (key, value, agent_id, updated_at)
            VALUES (?, ?, ?, ?)
        """, (key, val_str, agent_id, now))
        self.conn.commit()

    def retrieve(self, key: str) -> any:
        """Retrieve a fact from shared memory."""
        row = self.conn.execute("SELECT value FROM memory WHERE key=?", (key,)).fetchone()
        if row:
            return json.loads(row[0])
        return None

    def get_all(self) -> dict:
        """Get all facts in memory."""
        rows = self.conn.execute("SELECT key, value FROM memory").fetchall()
        return {row[0]: json.loads(row[1]) for row in rows}

    def clear(self):
        """Clear the memory."""
        self.conn.execute("DELETE FROM memory")
        self.conn.commit()

# Singleton instance
memory = SharedMemory()

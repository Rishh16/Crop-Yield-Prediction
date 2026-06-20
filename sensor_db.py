"""SQLite storage for IoT sensor readings (soil moisture, temperature, humidity)."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "sensor_data.db"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                soil_moisture REAL NOT NULL,
                temperature_c REAL NOT NULL,
                humidity_pct REAL NOT NULL
            )
            """
        )


def add_reading(soil_moisture: float, temperature_c: float, humidity_pct: float) -> None:
    init_db()
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with _conn() as c:
        c.execute(
            "INSERT INTO readings (created_at, soil_moisture, temperature_c, humidity_pct) VALUES (?,?,?,?)",
            (ts, soil_moisture, temperature_c, humidity_pct),
        )


def latest():
    init_db()
    with _conn() as c:
        row = c.execute(
            "SELECT id, created_at, soil_moisture, temperature_c, humidity_pct FROM readings ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def history(limit: int = 100):
    init_db()
    limit = max(1, min(int(limit), 500))
    with _conn() as c:
        rows = c.execute(
            """
            SELECT id, created_at, soil_moisture, temperature_c, humidity_pct
            FROM readings ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]
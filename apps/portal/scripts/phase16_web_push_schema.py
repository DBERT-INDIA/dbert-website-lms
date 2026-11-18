#!/usr/bin/env python3
"""
Phase 16: Native VAPID Web Push Devices & Delivery Telemetry Schema Migration
Creates web_push_devices and web_push_delivery_logs tables in PostgreSQL and SQLite.
Guarantees zero silent fails by tracking every push attempt with explicit event names and delivery statuses.
"""
import os
import sys

# Auto-load .env from apps/portal/.env if DATABASE_URL is not set
def load_env():
    portal_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(portal_dir, ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v

load_env()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database.adapter import get_db_adapter, PostgreSQLAdapter

SQL_POSTGRES = """
CREATE TABLE IF NOT EXISTS web_push_devices (
    id SERIAL PRIMARY KEY,
    intern_id INTEGER,
    user_email TEXT NOT NULL,
    endpoint TEXT NOT NULL UNIQUE,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    device_name TEXT NOT NULL,
    device_type TEXT DEFAULT 'desktop',
    user_agent TEXT,
    ip_address TEXT,
    is_active INTEGER DEFAULT 1,
    preferences TEXT DEFAULT '{"bounties": true, "sprints": true, "wallet": true, "attendance": true, "courses": true, "broadcasts": true}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_pushed_at TIMESTAMP WITH TIME ZONE,
    last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_web_push_intern ON web_push_devices(intern_id, is_active);
CREATE INDEX IF NOT EXISTS idx_web_push_email ON web_push_devices(user_email, is_active);
CREATE INDEX IF NOT EXISTS idx_web_push_active ON web_push_devices(is_active);

CREATE TABLE IF NOT EXISTS web_push_delivery_logs (
    id SERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    target_email TEXT NOT NULL,
    intern_id INTEGER,
    device_id INTEGER,
    title TEXT NOT NULL,
    body TEXT,
    target_url TEXT,
    status_code INTEGER,
    delivery_status TEXT NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_push_log_event ON web_push_delivery_logs(event_name, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_push_log_email ON web_push_delivery_logs(target_email, created_at DESC);
"""

SQL_SQLITE = """
CREATE TABLE IF NOT EXISTS web_push_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intern_id INTEGER,
    user_email TEXT NOT NULL,
    endpoint TEXT NOT NULL UNIQUE,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    device_name TEXT NOT NULL,
    device_type TEXT DEFAULT 'desktop',
    user_agent TEXT,
    ip_address TEXT,
    is_active INTEGER DEFAULT 1,
    preferences TEXT DEFAULT '{"bounties": true, "sprints": true, "wallet": true, "attendance": true, "courses": true, "broadcasts": true}',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_pushed_at TEXT,
    last_seen_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_web_push_intern ON web_push_devices(intern_id, is_active);
CREATE INDEX IF NOT EXISTS idx_web_push_email ON web_push_devices(user_email, is_active);
CREATE INDEX IF NOT EXISTS idx_web_push_active ON web_push_devices(is_active);

CREATE TABLE IF NOT EXISTS web_push_delivery_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    target_email TEXT NOT NULL,
    intern_id INTEGER,
    device_id INTEGER,
    title TEXT NOT NULL,
    body TEXT,
    target_url TEXT,
    status_code INTEGER,
    delivery_status TEXT NOT NULL,
    error_message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_push_log_event ON web_push_delivery_logs(event_name, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_push_log_email ON web_push_delivery_logs(target_email, created_at DESC);
"""

def run_migration():
    print("Running Phase 16: Web Push Devices & Telemetry Schema Migration...")
    db = get_db_adapter()
    is_pg = isinstance(db, PostgreSQLAdapter) or (hasattr(db, "_engine") and db._engine == "postgres")
    sql = SQL_POSTGRES if is_pg else SQL_SQLITE
    
    with db as conn:
        if is_pg:
            schema = os.environ.get("POSTGRES_SCHEMA", "dbert_internship")
            conn.execute(f"SET search_path TO {schema}, public;")
        
        for statement in sql.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                conn.execute(stmt)
        conn.commit()
    print("✓ Successfully created web_push_devices and web_push_delivery_logs tables!")

if __name__ == "__main__":
    run_migration()

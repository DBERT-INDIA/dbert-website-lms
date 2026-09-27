"""Tests for Phase 2: PostgreSQL-Only Enforcement."""

import os
import pytest
from services.database.adapter import get_db_adapter, PostgreSQLAdapter, DatabaseError

def test_require_postgres_raises_error_when_sqlite_attempted(monkeypatch):
    monkeypatch.setenv("REQUIRE_POSTGRES", "true")
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.setenv("DB_FILE", "test.db")

    with pytest.raises(RuntimeError) as exc_info:
        get_db_adapter("test.db")
    assert "PostgreSQL runtime database is enforced" in str(exc_info.value)

def test_postgres_url_returns_postgres_adapter():
    adapter = get_db_adapter("postgresql://user:pass@localhost:5432/dbert_lms")
    assert isinstance(adapter, PostgreSQLAdapter)

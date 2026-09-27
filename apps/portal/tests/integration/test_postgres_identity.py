import pytest
from services.database.adapter import get_db_adapter
import os

def test_postgres_search_path_enforcement(app):
    """
    Phase 1 Test: Ensure PostgreSQL search_path is strictly enforced on all connections
    and duplicate public tables do not intercept queries.
    """
    with app.app_context():
        # Only run if we are actually using Postgres (the app sets adapter type)
        adapter = get_db_adapter()
        if type(adapter).__name__ != 'PostgreSQLAdapter':
            pytest.skip("Test requires PostgreSQLAdapter")
            
        # Execute a raw query to check search_path
        with adapter.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SHOW search_path;")
            search_path = cur.fetchone()[0]
            
            # The adapter must enforce dbert_internship
            assert "dbert_internship" in search_path, f"search_path {search_path} missing target schema"

        # Ensure that intern_accounts exists ONLY in dbert_internship, not public
        with adapter.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(\"\"\"
                SELECT table_schema 
                FROM information_schema.tables 
                WHERE table_name = 'intern_accounts'
            \"\"\")
            schemas = [row[0] for row in cur.fetchall()]
            
            assert "dbert_internship" in schemas, "intern_accounts is missing from dbert_internship"
            assert "public" not in schemas, "Duplicate intern_accounts found in public schema (FK paradox risk)"

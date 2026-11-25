import sqlite3

from services.verified_portfolio import init_verified_portfolio, published_portfolio, write_portfolio_selection


def test_public_evidence_requires_selection_ownership_and_current_verification():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    try:
        init_verified_portfolio(conn)
        conn.executescript("""
            CREATE TABLE project_submissions (id INTEGER PRIMARY KEY, intern_id INTEGER, project_title TEXT,
                                              github_repo_url TEXT, status TEXT);
            CREATE TABLE intern_certificates (id INTEGER PRIMARY KEY, intern_id INTEGER, email TEXT,
                course_title TEXT, cert_id TEXT, issued_at TEXT, credential_status TEXT);
            INSERT INTO project_submissions VALUES
              (1, 1, 'Approved sample', 'https://github.com/example/approved', 'approved'),
              (2, 1, 'Pending sample', 'https://github.com/example/pending', 'pending'),
              (3, 2, 'Other learner', 'https://github.com/example/other', 'approved');
            INSERT INTO intern_certificates VALUES
              (1, 1, 'first@example.test', 'Credential', 'SAMPLE-ONE', '2026-11-23', 'valid'),
              (2, 1, 'first@example.test', 'Revoked', 'SAMPLE-TWO', '2026-11-23', 'revoked'),
              (3, 2, 'second@example.test', 'Other learner', 'SAMPLE-THREE', '2026-11-23', 'valid');
        """)
        assert published_portfolio(conn, 1, "first@example.test") == ([], [])
        write_portfolio_selection(conn, 1, {1, 2, 3}, {1, 2, 3})
        projects, certificates = published_portfolio(conn, 1, "first@example.test")
        assert [project["project_title"] for project in projects] == ["Approved sample"]
        assert [certificate["cert_id"] for certificate in certificates] == ["SAMPLE-ONE"]
        conn.execute("UPDATE intern_certificates SET credential_status='revoked' WHERE id=1")
        assert published_portfolio(conn, 1, "first@example.test")[1] == []
    finally:
        conn.close()

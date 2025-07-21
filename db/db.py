"""
db/db.py
Low-level helpers for the SQLite “feedback” database.
"""

from pathlib import Path
import sqlite3, textwrap

# ---------------------------------------------------------------------
#  File locations
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).parent            # …/CustomAgent_Smolagent/db
DB_PATH  = BASE_DIR / "feedback.db"         # …/db/feedback.db
SCHEMA_SQL = BASE_DIR / "feedback_schema.sql"

# ---------------------------------------------------------------------
#  Connection helper
# ---------------------------------------------------------------------
def connect() -> sqlite3.Connection:
    """Open the SQLite DB and ensure FK constraints are enforced."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ---------------------------------------------------------------------
#  One-time schema setup
# ---------------------------------------------------------------------
def init_schema() -> None:
    """Create tables if they don’t exist (idempotent)."""
    with connect() as conn, open(SCHEMA_SQL, "r", encoding="utf-8") as ddl:
        conn.executescript(ddl.read())

# ---------------------------------------------------------------------
#  High-level helpers (optional but handy)
# ---------------------------------------------------------------------
def save_submission(submission_name: str, files: list[dict]) -> int:
    """
    Insert a row into `submissions` and its related file rows.
    `files` is a list of dicts with keys 'fileName' and 'fullPath'.
    Returns the new submission_id.
    """
    with connect() as conn:
        cur = conn.execute(
            "INSERT INTO submissions (submission_name) VALUES (?)",
            (submission_name,),
        )
        submission_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO files (submission_id, file_name, full_path) VALUES (?,?,?)",
            [(submission_id, f["fileName"], f["fullPath"]) for f in files],
        )
    return submission_id


def log_feedback(file_id: int, tool_name: str, source: str, is_accepted: bool, comments: str) -> None:
    """Insert a feedback record with tool name."""
    with connect() as conn:
        conn.execute(
            "INSERT INTO feedback (file_id, tool_name, source, is_accepted, comments) VALUES (?,?,?,?,?)",
            (file_id, tool_name, source, is_accepted, comments),
        )


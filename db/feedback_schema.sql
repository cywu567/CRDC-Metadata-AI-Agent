-- db/feedback_schema.sql
CREATE TABLE IF NOT EXISTS submissions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_name TEXT    NOT NULL,
    ts              DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS files (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id   INTEGER NOT NULL,
    file_name       TEXT,
    full_path       TEXT,
    FOREIGN KEY (submission_id) REFERENCES submissions(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedback (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id     INTEGER NOT NULL,
    tool_name   TEXT    NOT NULL,
    source      TEXT    CHECK(source IN ('user','system')),
    is_accepted BOOLEAN,
    comments    TEXT,
    ts          DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(id)
        ON DELETE CASCADE
);
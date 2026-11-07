CREATE TABLE IF NOT EXISTS recitation_sessions(
 id INTEGER PRIMARY KEY,profile TEXT NOT NULL,work_id TEXT NOT NULL REFERENCES works(id),
 sentence_ids TEXT NOT NULL,mode TEXT NOT NULL CHECK(mode IN ('read','keywords','hidden')),
 self_rating TEXT NOT NULL CHECK(self_rating IN ('needs_practice','with_help','self_independent')),
 reveals INTEGER NOT NULL CHECK(reveals>=0),text_version TEXT NOT NULL,text_digest TEXT NOT NULL,
 created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS recitation_profile ON recitation_sessions(profile,created_at);
INSERT OR IGNORE INTO schema_migrations(version) VALUES(2);

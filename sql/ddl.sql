CREATE TABLE IF NOT EXISTS adverbs_adjectives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adjective_male TEXT UNIQUE,
    adjective_female TEXT UNIQUE,
    adjective_neutral TEXT UNIQUE,
    adverb TEXT UNIQUE,
    translation TEXT NOT NULL,
    comment TEXT,
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS nouns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT NOT NULL,
    word TEXT UNIQUE NOT NULL,
    translation TEXT NOT NULL,
    comment TEXT,
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);


CREATE TABLE IF NOT EXISTS verbs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL,
    translation TEXT NOT NULL,
    comment TEXT,
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL,
    number INTEGER UNIQUE NOT NULL,
    ordinal TEXT,
    comment TEXT,
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);
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
    gender TEXT NOT NULL CHECK (gender IN ('η', 'ο', 'το')),
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

CREATE TABLE IF NOT EXISTS prepositions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE NOT NULL,          
    translation TEXT NOT NULL,          
    comment TEXT,                       
    difficulty INTEGER NOT NULL DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS examples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL CHECK (table_name IN ('adverbs_adjectives', 'nouns', 'verbs', 'numbers', 'prepositions')),   -- The table being referenced: 'nouns', 'verbs', etc.
    word_id INTEGER NOT NULL,
    example_text TEXT NOT NULL, 
    translation TEXT,           
    comment TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(table_name, word_id, example_text)
);

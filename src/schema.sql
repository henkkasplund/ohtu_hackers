CREATE TABLE IF NOT EXISTS reference_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    citation_key TEXT NOT NULL UNIQUE,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    booktitle TEXT,
    journal TEXT,
    volume TEXT,
    pages TEXT,
    publisher TEXT,
    reference_type_name TEXT NOT NULL,
    FOREIGN KEY (reference_type_name) REFERENCES reference_types(name)
);
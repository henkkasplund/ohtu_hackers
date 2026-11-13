CREATE TABLE IF NOT EXISTS citation_styles (
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
    citation_style_name TEXT NOT NULL,
    FOREIGN KEY (citation_style_name) REFERENCES citation_styles(name)
);
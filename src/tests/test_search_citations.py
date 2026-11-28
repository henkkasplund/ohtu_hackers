import os
import unittest

from sqlalchemy import text

from config import app, db
from entities.citation import Citation
from repositories.citation_repository import search_citations

os.environ["DATABASE_URL"] = "sqlite:///:memory:"


class TestSearchCitations(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        db.session.execute(
            text("""
                CREATE TABLE IF NOT EXISTS reference_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    display_name TEXT NOT NULL
                )
            """)
        )
        db.session.execute(
            text("""
                CREATE TABLE IF NOT EXISTS citations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    citation_key TEXT UNIQUE NOT NULL,
                    tag TEXT NOT NULL,
                    author TEXT NOT NULL,
                    title TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    publisher TEXT,
                    booktitle TEXT,
                    journal TEXT,
                    volume TEXT,
                    pages TEXT,
                    reference_type_name TEXT NOT NULL
                )
            """)
        )
        db.session.execute(text("DELETE FROM citations"))
        db.session.execute(text("DELETE FROM reference_types"))
        db.session.execute(
            text("""
                INSERT INTO reference_types (name, display_name)
                VALUES
                    ('book', 'Kirja'),
                    ('article', 'Artikkeli'),
                    ('inproceedings', 'Konferenssijulkaisu')
            """)
        )
        db.session.execute(
            text("""
                INSERT INTO citations (
                    citation_key, tag, author, title, year, publisher, reference_type_name
                )
                VALUES
                    ('Jesse08', 'Gradu', 'Roope Ojala', 'PuuSaunat', 2008, 'Otava', 'book'),
                    ('Kalle18', 'Gradu', 'Hessu Tassu', 'Reissumies', 2018, 'Ressu', 'book'),
                    ('Markku97', 'Gradu', 'Väinö Kontti', 'Juusto ja Viini', 1997, 'FineDining', 'book')
            """)
        )
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.engine.dispose()
        self.app_context.pop()

    def test_search_by_author_case_insensitive_partial_match(self):
        results = search_citations(author="roope")
        keys = [ref.citation_key for ref in results]
        self.assertEqual(keys, ["Jesse08"])
        self.assertNotIn("Kalle18", keys)
        self.assertNotIn("Markku97", keys)
        self.assertTrue(all(isinstance(ref, Citation) for ref in results))

    def test_search_by_year(self):
        results = search_citations(year=2008)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].citation_key, "Jesse08")
        self.assertEqual(results[0].tag, "Gradu")
        self.assertEqual(results[0].author, "Roope Ojala")
        self.assertEqual(results[0].reference_type_display_name, "Kirja")

    def test_search_by_author_and_year(self):
        results = search_citations(author="Hessu", year=2018)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].tag, "Gradu")
        self.assertEqual(results[0].author, "Hessu Tassu")
        self.assertEqual(results[0].citation_key, "Kalle18")

        no_match = search_citations(author="Hessu", year=2008)
        self.assertEqual(no_match, [])

        empty = search_citations(author="Väinö", year=2018)
        self.assertEqual(empty, [])

    def test_search_with_no_filters_returns_all(self):
        results = search_citations()
        self.assertEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()

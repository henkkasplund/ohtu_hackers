import unittest

from bibtex import create_bibtex
from entities.citation import Citation


class TestBibtexCreation(unittest.TestCase):
    def setUp(self):
        self.book = Citation(
            citation_key="Martin09",
            author="Robert Martin",
            title="Clean Code",
            year=2008,
            reference_type_name="book",
            publisher="Prentice Hall",
        )

    def test_bibtex_creates_correct_bibtex(self):
        expected = (
            "@book{Martin09,\n"
            "  author = {Robert Martin},\n"
            "  title = {Clean Code},\n"
            "  year = {2008},\n"
            "  publisher = {Prentice Hall}\n"
            "}"
        )
        self.assertEqual(create_bibtex(self.book), expected)

    def test_empty_fields_are_omitted(self):
        comparable = create_bibtex(self.book)
        self.assertNotIn("journal", comparable)
        self.assertNotIn("volume", comparable)
        self.assertNotIn("pages", comparable)
        self.assertNotIn("None", comparable)

    def test_string_works_as_year(self):
        self.book.year = "1990"
        self.assertIn("year = {1990}", create_bibtex(self.book))

    def test_article_fields_included(self):
        article = Citation(
            citation_key="Martin09",
            author="Robert Martin",
            title="Clean Code",
            year=2008,
            reference_type_name="article",
            journal="Testing Journal",
            volume="10",
            pages="27--29",
        )
        comparable = create_bibtex(article)
        self.assertTrue(comparable.startswith("@article{Martin09,"))
        self.assertIn("journal = {Testing Journal}", comparable)
        self.assertIn("pages = {27--29}", comparable)
        self.assertNotIn("publisher", comparable)

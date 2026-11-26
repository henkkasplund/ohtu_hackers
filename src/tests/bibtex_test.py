import unittest

from bibtex import create_bibtex, create_bibtex_file
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


class TestBibtexFileCreation(unittest.TestCase):
    def setUp(self):
        self.book = Citation(
            citation_key="Martin09",
            author="Robert Martin",
            title="Clean Code",
            year=2008,
            reference_type_name="book",
            publisher="Prentice Hall",
        )
        self.article = Citation(
            citation_key="CBH91",
            author="Allan Collins",
            title="Cognitive apprenticeship",
            year=1991,
            reference_type_name="article",
            journal="American Educator",
            volume="6",
            pages="38--46",
        )

    def test_empty_list_returns_empty_string(self):
        self.assertEqual(create_bibtex_file([]), "")

    def test_single_reference_matches_create_bibtex(self):
        self.assertEqual(create_bibtex_file([self.book]), create_bibtex(self.book))

    def test_references_are_separated_by_blank_line(self):
        result = create_bibtex_file([self.book, self.article])
        expected = create_bibtex(self.book) + "\n\n" + create_bibtex(self.article)
        self.assertEqual(result, expected)

    def test_all_reference_types_are_included(self):
        result = create_bibtex_file([self.book, self.article])
        self.assertIn("@book{Martin09,", result)
        self.assertIn("@article{CBH91,", result)
        self.assertIn("journal = {American Educator}", result)

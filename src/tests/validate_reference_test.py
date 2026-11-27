import unittest
from unittest.mock import patch

from entities.citation import Citation
from util import UserInputError, validate_reference


class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        self.valid_book = Citation(
            citation_key="Martin2008",
            tag="Gradu",
            author="Robert C. Martin",
            title="Clean Code",
            year="2008",
            publisher="Prentice Hall",
            reference_type_name="book",
        )
        self.valid_article = Citation(
            citation_key="CBH91",
            tag="Gradu",
            author="Allan Collins and John Seely Brown and Ann Holum",
            title="Cognitive apprenticeship: making thinking visible",
            journal="American Educator",
            year="1991",
            volume="6",
            pages="38--46",
            reference_type_name="article",
        )
        self.valid_inproceedings = Citation(
            citation_key="VPL11",
            author="Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
            title=(
                "Extreme Apprenticeship Method in Teaching Programming "
                "for Beginners."
            ),
            year="2011",
            booktitle=(
                "SIGCSE '11: Proceedings of the 42nd SIGCSE technical "
                "symposium on Computer science education"
            ),
            reference_type_name="inproceedings",
        )

    @patch("util.citation_repository.citation_key_exists", return_value=False)
    def test_valid_book_does_not_raise_error(self, mock_exists):
        validate_reference(self.valid_book)
        mock_exists.assert_called_once_with("Martin2008")

    @patch("util.citation_repository.citation_key_exists", return_value=True)
    def test_duplicate_citation_key_raises_error(self, _mock_exists):
        with self.assertRaises(UserInputError):
            validate_reference(self.valid_book)

    @patch(
        "util.citation_repository.citation_key_exists_except",
        return_value=False,
    )
    def test_edit_allows_existing_key_when_no_other_reference_uses_it(
        self, mock_exists
    ):
        validate_reference(self.valid_book, exclude_citation_id=42)

        mock_exists.assert_called_once_with("Martin2008", 42)

    @patch(
        "util.citation_repository.citation_key_exists_except",
        return_value=True,
    )
    def test_edit_rejects_key_used_by_another_reference(self, mock_exists):
        with self.assertRaises(UserInputError):
            validate_reference(self.valid_book, exclude_citation_id=42)

        mock_exists.assert_called_once_with("Martin2008", 42)

    def test_missing_field_raises_error(self):
        self.valid_book.author = "   "

        with self.assertRaises(UserInputError):
            validate_reference(self.valid_book)

    def test_invalid_year_raises_error(self):
        self.valid_book.year = "3000"

        with self.assertRaises(UserInputError):
            validate_reference(self.valid_book)

    def test_unknown_style_raises_error(self):
        self.valid_book.reference_type_name = "UnknownStyle"
        with self.assertRaises(UserInputError):
            validate_reference(self.valid_book)

    @patch("util.citation_repository.citation_key_exists", return_value=False)
    def test_valid_article_without_optional_fields(self, mock_exists):
        self.valid_article.volume = ""
        self.valid_article.pages = ""

        validate_reference(self.valid_article)
        mock_exists.assert_called_once_with("CBH91")

    @patch("util.citation_repository.citation_key_exists", return_value=False)
    def test_valid_article_with_optional_fields(self, mock_exists):
        validate_reference(self.valid_article)
        mock_exists.assert_called_once_with("CBH91")

    @patch("util.citation_repository.citation_key_exists", return_value=True)
    def test_duplicate_article_key_raises_error(self, _mock_exists):
        with self.assertRaises(UserInputError):
            validate_reference(self.valid_article)

    def test_missing_required_article_field_raises_error(self):
        for field in (
            "citation_key",
            "tag",
            "author",
            "title",
            "journal",
            "year",
        ):
            original_value = getattr(self.valid_article, field)
            setattr(self.valid_article, field, "   ")

            with self.subTest(field=field), self.assertRaises(UserInputError):
                validate_reference(self.valid_article)

            setattr(self.valid_article, field, original_value)

    def test_invalid_article_year_raises_error(self):
        for year in ("0", "-1", "1991.5", "ei-luku", "3000"):
            with self.subTest(year=year), self.assertRaises(UserInputError):
                self.valid_article.year = year
                validate_reference(self.valid_article)

    def test_missing_book_tag_raises_error(self):
        self.valid_book.tag = "   "

        with self.assertRaises(UserInputError):
            validate_reference(self.valid_book)

    @patch("util.citation_repository.citation_key_exists", return_value=False)
    def test_valid_inproceedings_does_not_raise_error(self, mock_exists):
        validate_reference(self.valid_inproceedings)
        mock_exists.assert_called_once_with("VPL11")

    def test_missing_inproceedings_booktitle_raises_error(self):
        self.valid_inproceedings.booktitle = "   "

        with self.assertRaises(UserInputError):
            validate_reference(self.valid_inproceedings)

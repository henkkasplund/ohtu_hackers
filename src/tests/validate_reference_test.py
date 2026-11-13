import unittest
from unittest.mock import patch

from util import UserInputError, validate_reference


class TestReferenceValidation(unittest.TestCase):
    def setUp(self):
        self.valid_book = {
            "citation_key": "Martin2008",
            "author": "Robert C. Martin",
            "title": "Clean Code",
            "year": "2008",
            "publisher": "Prentice Hall",
        }

    @patch("util.citation_repository.citation_key_exists", return_value=False)
    def test_valid_book_does_not_raise_error(self, mock_exists):
        validate_reference("Kirja", self.valid_book)
        mock_exists.assert_called_once_with("Martin2008")

    @patch("util.citation_repository.citation_key_exists", return_value=True)
    def test_duplicate_citation_key_raises_error(self, mock_exists):
        with self.assertRaises(UserInputError):
            validate_reference("Kirja", self.valid_book)

    def test_missing_field_raises_error(self):
        invalid_book = self.valid_book.copy()
        invalid_book["author"] = "   "

        with self.assertRaises(UserInputError):
            validate_reference("Kirja", invalid_book)

    def test_invalid_year_raises_error(self):
        invalid_book = self.valid_book.copy()
        invalid_book["year"] = "3000"

        with self.assertRaises(UserInputError):
            validate_reference("Kirja", invalid_book)

    def test_unknown_style_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference("A", self.valid_book)

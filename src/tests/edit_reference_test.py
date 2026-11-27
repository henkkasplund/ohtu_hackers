import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app import app
from entities.citation import Citation


class TestReferenceEditing(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.citation_id = 42
        self.reference = Citation(
            citation_id=self.citation_id,
            citation_key="Martin09",
            author="Robert Martin",
            title="Clean Code",
            year="2008",
            reference_type_name="book",
            publisher="Prentice Hall",
            reference_type_display_name="Kirja",
        )
        self.article_reference = Citation(
            citation_id=self.citation_id,
            citation_key="Collins91",
            author="Allan Collins",
            title="Cognitive apprenticeship",
            year="1991",
            reference_type_name="article",
            journal="American Educator",
            volume="6",
            pages="38--46",
            reference_type_display_name="Artikkeli",
        )
        self.path = f"/references/{self.citation_id}/edit_reference"

    def test_get_edit_form_shows_existing_reference(self):
        reference_types = [
            SimpleNamespace(name="book", display_name="Kirja"),
            SimpleNamespace(name="article", display_name="Artikkeli"),
        ]
        with (
            patch(
                "app.citation_repository.get_citation_by_id",
                return_value=self.reference,
            ) as get_citation,
            patch(
                "app.citation_repository.get_reference_types",
                return_value=reference_types,
            ),
        ):
            response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Viitetyyppi: Kirja", response.data)
        self.assertIn(b'value="Martin09"', response.data)
        self.assertNotIn(b"<select", response.data)
        get_citation.assert_called_once_with(self.citation_id)

    def test_get_edit_form_returns_404_for_missing_reference(self):
        with patch(
            "app.citation_repository.get_citation_by_id", return_value=None
        ):
            response = self.client.get(self.path)

        self.assertEqual(response.status_code, 404)

    def test_post_updates_book(self):
        form_data = {
            "reference_type_name": "book",
            "citation_key": "Martin10",
            "author": "Robert Martin",
            "title": "Clean Coder",
            "year": "2011",
            "publisher": "Prentice Hall",
        }
        with (
            patch(
                "app.citation_repository.get_citation_by_id",
                return_value=self.reference,
            ),
            patch("app.util.validate_reference") as validate_reference,
            patch("app.citation_repository.update_book") as update_book,
        ):
            response = self.client.post(self.path, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], f"/references/{self.citation_id}")
        updated_book = update_book.call_args.args[1]
        update_book.assert_called_once_with(self.citation_id, updated_book)
        validate_reference.assert_called_once_with(
            updated_book, exclude_citation_id=self.citation_id
        )
        self.assertEqual(updated_book.citation_key, "Martin10")
        self.assertEqual(updated_book.reference_type_name, "book")

    def test_post_updates_article(self):
        form_data = {
            "reference_type_name": "article",
            "citation_key": "Collins91",
            "author": "Allan Collins",
            "title": "Cognitive apprenticeship",
            "year": "1991",
            "journal": "American Educator",
            "volume": "6",
            "pages": "38--46",
        }
        with (
            patch(
                "app.citation_repository.get_citation_by_id",
                return_value=self.article_reference,
            ),
            patch("app.util.validate_reference") as validate_reference,
            patch("app.citation_repository.update_article") as update_article,
        ):
            response = self.client.post(self.path, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"], f"/references/{self.citation_id}"
        )
        updated_article = update_article.call_args.args[1]
        update_article.assert_called_once_with(self.citation_id, updated_article)
        validate_reference.assert_called_once_with(
            updated_article, exclude_citation_id=self.citation_id
        )
        self.assertEqual(updated_article.citation_key, "Collins91")
        self.assertEqual(updated_article.reference_type_name, "article")

    def test_post_rejects_unknown_reference_type(self):
        with (
            patch(
                "app.citation_repository.get_citation_by_id",
                return_value=self.reference,
            ),
            patch("app.citation_repository.update_book") as update_book,
            patch("app.citation_repository.update_article") as update_article,
        ):
            response = self.client.post(
                self.path,
                data={"reference_type_name": "unknown"},
            )

        self.assertEqual(response.status_code, 400)
        update_book.assert_not_called()
        update_article.assert_not_called()


if __name__ == "__main__":
    unittest.main()

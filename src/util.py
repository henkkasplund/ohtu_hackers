from datetime import datetime

from entities.citation import Citation
from repositories import citation_repository


class UserInputError(Exception):
    pass


def validate_todo(content):
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
        raise UserInputError("Todo content length must be smaller than 100")


def create_book_citation(form_data):
    citation_key = form_data.get("citation_key", "").strip()
    author = form_data.get("author", "").strip()
    title = form_data.get("title", "").strip()
    year = form_data.get("year", "").strip()
    publisher = form_data.get("publisher", "").strip()

    return Citation(
        citation_key=citation_key,
        author=author,
        title=title,
        year=year,
        reference_type_name="book",
        publisher=publisher,
    )


def validate_reference(citation, exclude_citation_id=None):
    if citation.reference_type_name == "book":
        required_fields = [
            citation.citation_key,
            citation.author,
            citation.title,
            citation.year,
            citation.publisher,
        ]
        for value in required_fields:
            if not value or not value.strip():
                raise UserInputError("Kaikki kirjan kentät ovat pakollisia!")

        current_year = datetime.now().year
        if not citation.year.isdigit() or not (
            0 <= int(citation.year) <= current_year
        ):
            raise UserInputError(
                f"Vuoden täytyy olla kokonaisluku väliltä 1–{current_year}"
            )
    else:
        raise UserInputError("Tuntematon viitetyyppi!")

    if exclude_citation_id is None:
        duplicate_exists = citation_repository.citation_key_exists(
            citation.citation_key
        )
    else:
        duplicate_exists = citation_repository.citation_key_exists_except(
            citation.citation_key,
            exclude_citation_id,
        )

    if duplicate_exists:
        raise UserInputError(
            f"Viiteavain '{citation.citation_key}' on jo käytössä!"
        )

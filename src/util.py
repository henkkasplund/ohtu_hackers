import re
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
    tag = form_data.get("tag_name", "").strip()
    author = form_data.get("author", "").strip()
    title = form_data.get("title", "").strip()
    year = form_data.get("year", "").strip()
    publisher = form_data.get("publisher", "").strip()

    return Citation(
        citation_key=citation_key,
        tag=tag,
        author=author,
        title=title,
        year=year,
        reference_type_name="book",
        publisher=publisher,
    )


def create_article_citation(form_data):
    citation_key = form_data.get("citation_key", "").strip()
    tag = form_data.get("tag_name", "").strip()
    author = form_data.get("author", "").strip()
    title = form_data.get("title", "").strip()
    year = form_data.get("year", "").strip()
    journal = form_data.get("journal", "").strip()
    volume = form_data.get("volume", "").strip()
    pages = form_data.get("pages", "").strip()

    return Citation(
        citation_key=citation_key,
        tag=tag,
        author=author,
        title=title,
        year=year,
        reference_type_name="article",
        journal=journal,
        volume=volume,
        pages=pages,
    )


def create_inproceedings_citation(form_data):
    citation_key = form_data.get("citation_key", "").strip()
    tag = form_data.get("tag_name", "").strip()
    author = form_data.get("author", "").strip()
    title = form_data.get("title", "").strip()
    year = form_data.get("year", "").strip()
    booktitle = form_data.get("booktitle", "").strip()

    return Citation(
        citation_key=citation_key,
        tag=tag,
        author=author,
        title=title,
        year=year,
        reference_type_name="inproceedings",
        booktitle=booktitle,
    )


def validate_volume_and_pages(citation):
    if citation.volume and (
        not citation.volume.isdecimal() or int(citation.volume) <= 0
    ):
        raise UserInputError(
            "Vuosikerran täytyy olla positiivinen kokonaisluku!"
        )

    if (
        citation.pages
        and re.fullmatch(r"[0-9]+(-{1,2}[0-9]+)?", citation.pages) is None
    ):
        raise UserInputError(
            "Anna sivunumero tai sivuväli (esim. 38 tai 38-46)!"
        )


def validate_reference(citation, exclude_citation_id=None):
    if citation.reference_type_name == "book":
        required_fields = [
            citation.citation_key,
            citation.tag,
            citation.author,
            citation.title,
            citation.year,
            citation.publisher,
        ]
        missing_fields_message = "Kaikki kirjan kentät ovat pakollisia!"
    elif citation.reference_type_name == "article":
        required_fields = [
            citation.citation_key,
            citation.tag,
            citation.author,
            citation.title,
            citation.journal,
            citation.year,
        ]
        missing_fields_message = (
            "Artikkelin avain, tekijä, otsikko, lehti ja vuosi ovat pakollisia!"
        )
    elif citation.reference_type_name == "inproceedings":
        required_fields = [
            citation.citation_key,
            citation.tag,
            citation.author,
            citation.title,
            citation.booktitle,
            citation.year,
        ]
        missing_fields_message = (
            "Konferenssiviitteen kaikki kentät ovat pakollisia!"
        )
    else:
        raise UserInputError("Tuntematon viitetyyppi!")

    for value in required_fields:
        if not value or not value.strip():
            raise UserInputError(missing_fields_message)

    current_year = datetime.now().year
    if not citation.year.isdigit() or not (
        1 <= int(citation.year) <= current_year
    ):
        raise UserInputError(
            f"Vuoden täytyy olla kokonaisluku väliltä 1–{current_year}"
        )

    if citation.reference_type_name == "article":
        validate_volume_and_pages(citation)

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

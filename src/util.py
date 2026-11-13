from datetime import datetime

from repositories import citation_repository


class UserInputError(Exception):
    pass


def validate_todo(content):
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
        raise UserInputError("Todo content length must be smaller than 100")


def validate_reference(style_name, form_data):
    if style_name == "Kirja":
        required_fields = [
            "citation_key",
            "author",
            "title",
            "year",
            "publisher",
        ]
        for field in required_fields:
            value = form_data.get(field)
            if not value or not value.strip():
                raise UserInputError("Kaikki kirjan kentät ovat pakollisia!")

        year = form_data.get("year", "").strip()
        current_year = datetime.now().year
        if not year.isdigit() or not (1 <= int(year) <= current_year):
            raise UserInputError(
                f"Vuoden täytyy olla kokonaisluku väliltä 1–{current_year}!"
            )
    else:
        raise UserInputError("Tuntematon viitetyyppi!")
    citation_key = form_data.get("citation_key", "").strip()
    if citation_repository.citation_key_exists(citation_key):
        raise UserInputError(f"Viiteavain '{citation_key}' on jo käytössä!")

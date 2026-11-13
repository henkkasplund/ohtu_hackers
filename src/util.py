from sqlalchemy import text

from config import db


class UserInputError(Exception):
    pass


def validate_todo(content):
    if len(content) < 5:
        raise UserInputError("Todo content length must be greater than 4")

    if len(content) > 100:
        raise UserInputError("Todo content length must be smaller than 100")


def get_citation_styles():
    result = db.session.execute(text("SELECT id, name FROM citation_styles"))
    return result.fetchall()


def validate_reference(style_name, form_data):
    if style_name == "Kirja":
        required_fields = [
            "citation_key",
            "author",
            "title",
            "year",
            "publisher",
        ]
        year = form_data.get("year", "").strip()
        if not year.isdigit() or int(year) <= 0:
            raise UserInputError(
                "Vuoden täytyy olla positiivinen kokonaisluku!"
            )
        for field in required_fields:
            value = form_data.get(field)
            if not value or not value.strip():
                raise UserInputError("Kaikki kirjan kentät ovat pakollisia!")
    else:
        raise UserInputError("Tuntematon viitetyyppi!")

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

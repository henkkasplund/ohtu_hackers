from sqlalchemy import text

from config import db
from entities.citation import Citation


def set_done(todo_id):
    sql = text("UPDATE todos SET done = TRUE WHERE id = :id")
    db.session.execute(sql, {"id": todo_id})
    db.session.commit()


def create_todo(content):
    sql = text("INSERT INTO todos (content) VALUES (:content)")
    db.session.execute(sql, {"content": content})
    db.session.commit()


def get_reference_types():
    result = db.session.execute(text("SELECT id, name FROM reference_types"))
    return result.fetchall()


def get_all_citations():
    result = db.session.execute(
        text("""
            SELECT id, citation_key, author, title, year, publisher, reference_type_name
            FROM citations
        """)
    )
    citations = result.fetchall()
    return [
        Citation(
            citation_id=row.id,
            citation_key=row.citation_key,
            author=row.author,
            title=row.title,
            year=row.year,
            publisher=row.publisher,
            reference_type_name=row.reference_type_name,
        )
        for row in citations
    ]


def save_book(book):
    sql = text("""
        INSERT INTO citations (
            citation_key, author, title, year, publisher, reference_type_name
        )
        VALUES (
            :citation_key, :author, :title, :year, :publisher, :reference_type_name
        )
    """)
    db.session.execute(
        sql,
        {
            "citation_key": book.citation_key,
            "author": book.author,
            "title": book.title,
            "year": int(book.year),
            "publisher": book.publisher,
            "reference_type_name": book.reference_type_name,
        },
    )
    db.session.commit()


def citation_key_exists(citation_key):
    sql = text("SELECT 1 FROM citations WHERE citation_key = :citation_key")
    result = db.session.execute(sql, {"citation_key": citation_key}).fetchone()
    return result is not None

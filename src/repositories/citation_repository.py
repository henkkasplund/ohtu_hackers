from sqlalchemy import text

from config import db
from entities.todo import Todo


def get_todos():
    result = db.session.execute(text("SELECT id, content, done FROM todos"))
    todos = result.fetchall()
    return [Todo(todo[0], todo[1], todo[2]) for todo in todos]


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
    return result.fetchall()


def create_book(citation_key, author, title, year, publisher, style_name):
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
            "citation_key": citation_key,
            "author": author,
            "title": title,
            "year": int(year),
            "publisher": publisher,
            "reference_type_name": style_name,
        },
    )
    db.session.commit()

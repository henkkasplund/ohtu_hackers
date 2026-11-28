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
    result = db.session.execute(
        text("SELECT id, name, display_name FROM reference_types")
    )
    return result.fetchall()


def get_all_citations():
    result = db.session.execute(
        text("""
            SELECT c.id, c.citation_key, c.tag, c.author, c.title, c.year, c.publisher,
            c.booktitle, c.journal, c.volume, c.pages,
            c.reference_type_name, rt.display_name
            FROM citations c
            JOIN reference_types rt ON c.reference_type_name = rt.name
        """)
    )
    citations = result.fetchall()
    return [
        Citation(
            citation_id=row.id,
            citation_key=row.citation_key,
            tag=row.tag,
            author=row.author,
            title=row.title,
            year=row.year,
            publisher=row.publisher,
            booktitle=row.booktitle,
            journal=row.journal,
            volume=row.volume,
            pages=row.pages,
            reference_type_name=row.reference_type_name,
            reference_type_display_name=row.display_name,
        )
        for row in citations
    ]


def save_book(book):
    sql = text("""
        INSERT INTO citations (
            citation_key, tag, author, title, year, publisher, reference_type_name
        )
        VALUES (
            :citation_key, :tag, :author, :title, :year, :publisher, :reference_type_name
        )
    """)
    db.session.execute(
        sql,
        {
            "citation_key": book.citation_key,
            "tag": book.tag,
            "author": book.author,
            "title": book.title,
            "year": int(book.year),
            "publisher": book.publisher,
            "reference_type_name": book.reference_type_name,
        },
    )
    db.session.commit()


def save_article(article):
    sql = text("""
        INSERT INTO citations (
            citation_key, tag, author, title, year,
            journal, volume, pages, reference_type_name
        )
        VALUES (
            :citation_key, :tag, :author, :title, :year,
            :journal, :volume, :pages, :reference_type_name
        )
    """)
    db.session.execute(
        sql,
        {
            "citation_key": article.citation_key,
            "tag": article.tag,
            "author": article.author,
            "title": article.title,
            "year": int(article.year),
            "journal": article.journal,
            "volume": article.volume,
            "pages": article.pages,
            "reference_type_name": article.reference_type_name,
        },
    )
    db.session.commit()


def save_inproceedings(inproceedings):
    sql = text("""
        INSERT INTO citations (
            citation_key, tag, author, title, year,
            booktitle, reference_type_name
        )
        VALUES (
            :citation_key, :tag, :author, :title, :year,
            :booktitle, :reference_type_name
        )
    """)
    db.session.execute(
        sql,
        {
            "citation_key": inproceedings.citation_key,
            "tag": inproceedings.tag,
            "author": inproceedings.author,
            "title": inproceedings.title,
            "year": int(inproceedings.year),
            "booktitle": inproceedings.booktitle,
            "reference_type_name": inproceedings.reference_type_name,
        },
    )
    db.session.commit()


def citation_key_exists(citation_key):
    sql = text("SELECT 1 FROM citations WHERE citation_key = :citation_key")
    result = db.session.execute(sql, {"citation_key": citation_key}).fetchone()
    return result is not None


def citation_key_exists_except(citation_key, citation_id):
    sql = text("""
        SELECT 1 FROM citations
        WHERE citation_key = :citation_key AND id != :citation_id
    """)
    result = db.session.execute(
        sql,
        {"citation_key": citation_key, "citation_id": citation_id},
    ).fetchone()
    return result is not None


def get_citation_by_id(citation_id):
    sql = text("""
        SELECT c.id, c.citation_key, c.tag, c.author, c.title, c.year, c.publisher,
               c.booktitle, c.journal, c.volume, c.pages,
               c.reference_type_name, rt.display_name
        FROM citations c
        JOIN reference_types rt ON c.reference_type_name = rt.name
        WHERE c.id = :id
    """)
    row = db.session.execute(sql, {"id": citation_id}).fetchone()

    if row is None:
        return None

    return Citation(
        citation_id=row.id,
        citation_key=row.citation_key,
        tag=row.tag,
        author=row.author,
        title=row.title,
        year=row.year,
        publisher=row.publisher,
        booktitle=row.booktitle,
        journal=row.journal,
        volume=row.volume,
        pages=row.pages,
        reference_type_name=row.reference_type_name,
        reference_type_display_name=row.display_name,
    )


def update_book(citation_id, book):
    sql = text("""
        UPDATE citations
        SET citation_key = :citation_key,
            tag = :tag,
            author = :author,
            title = :title,
            year = :year,
            publisher = :publisher,
            reference_type_name = :reference_type_name
        WHERE id = :citation_id
    """)
    db.session.execute(
        sql,
        {
            "citation_id": citation_id,
            "citation_key": book.citation_key,
            "tag": book.tag,
            "author": book.author,
            "title": book.title,
            "year": int(book.year),
            "publisher": book.publisher,
            "reference_type_name": book.reference_type_name,
        },
    )
    db.session.commit()


def update_article(citation_id, article):
    sql = text("""
        UPDATE citations
        SET citation_key = :citation_key,
            tag = :tag,
            author = :author,
            title = :title,
            year = :year,
            journal = :journal,
            volume = :volume,
            pages = :pages,
            reference_type_name = :reference_type_name
        WHERE id = :citation_id
    """)
    db.session.execute(
        sql,
        {
            "citation_id": citation_id,
            "citation_key": article.citation_key,
            "tag": article.tag,
            "author": article.author,
            "title": article.title,
            "year": int(article.year),
            "journal": article.journal,
            "volume": article.volume,
            "pages": article.pages,
            "reference_type_name": article.reference_type_name,
        },
    )
    db.session.commit()


def update_inproceedings(citation_id, inproceedings):
    sql = text("""
        UPDATE citations
        SET citation_key = :citation_key,
            tag = :tag,
            author = :author,
            title = :title,
            year = :year,
            booktitle = :booktitle,
            reference_type_name = :reference_type_name
        WHERE id = :citation_id
    """)
    db.session.execute(
        sql,
        {
            "citation_id": citation_id,
            "citation_key": inproceedings.citation_key,
            "tag": inproceedings.tag,
            "author": inproceedings.author,
            "title": inproceedings.title,
            "year": int(inproceedings.year),
            "booktitle": inproceedings.booktitle,
            "reference_type_name": inproceedings.reference_type_name,
        },
    )
    db.session.commit()


def delete_citation(citation_id):
    sql = text("DELETE FROM citations WHERE id = :id")
    db.session.execute(sql, {"id": citation_id})
    db.session.commit()


def add_tag(tag_name):
    sql = text("INSERT INTO tags (name) VALUES (:name)")
    db.session.execute(sql, {"name": tag_name})
    db.session.commit()


def get_all_tags():
    sql = text("SELECT id, name FROM tags")
    return db.session.execute(sql).fetchall()


def search_citations(author=None, year=None):
    conditions = []
    params = {}

    if author:
        conditions.append("LOWER(c.author) LIKE :author")
        params["author"] = f"%{author.strip().lower()}%"

    if year is not None:
        conditions.append("c.year = :year")
        params["year"] = year

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    sql = text(f"""
        SELECT c.id, c.citation_key, c.tag, c.author, c.title, c.year, c.publisher,
        c.booktitle, c.journal, c.volume, c.pages,
        c.reference_type_name, rt.display_name
        FROM citations c
        JOIN reference_types rt ON c.reference_type_name = rt.name
        {where_clause}
        ORDER BY c.id DESC
    """)

    citations = db.session.execute(sql, params).fetchall()
    return [
        Citation(
            citation_id=row.id,
            citation_key=row.citation_key,
            tag=row.tag,
            author=row.author,
            title=row.title,
            year=row.year,
            publisher=row.publisher,
            booktitle=row.booktitle,
            journal=row.journal,
            volume=row.volume,
            pages=row.pages,
            reference_type_name=row.reference_type_name,
            reference_type_display_name=row.display_name,
        )
        for row in citations
    ]

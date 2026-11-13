import os

from sqlalchemy import text

from config import app, db


def reset_db():
    print("Clearing contents from table todos")
    sql = text("DELETE FROM todos")
    db.session.execute(sql)
    db.session.commit()


def tables():
    """Returns all table names from the database"""
    sql = text(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def setup_db():
    """
    Creating the database
    If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    # Read schema from schema.sql file
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read().strip()

    for statement in schema_sql.split(";"):
        if statement.strip():
            db.session.execute(text(statement))
    db.session.commit()

    # Read initial data from init.sql file
    init_path = os.path.join(os.path.dirname(__file__), "init.sql")
    if os.path.exists(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            init_sql = f.read().strip()

        for statement in init_sql.split(";"):
            if statement.strip():
                db.session.execute(text(statement))
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()

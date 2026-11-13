from flask import flash, jsonify, redirect, render_template, request

import util
from config import app, test_env
from db_helper import reset_db
from repositories.todo_repository import create_todo, set_done


## @app.route("/")
## def index():
## todos = get_todos()
## unfinished = len([todo for todo in todos if not todo.done])
## return render_template("index.html", todos=todos, unfinished=unfinished)
@app.route("/")
def index():

    return render_template(
        "index.html",
    )


@app.route("/add_reference", methods=["GET", "POST"])
def add_reference():
    if request.method == "POST":
        style_name = request.form.get("reference_types_name")

        if style_name == "Kirja":
            required_fields = [
                "citation_key",
                "author",
                "title",
                "year",
                "publisher",
            ]
            if not all(request.form.get(field) for field in required_fields):
                return "Kaikki kirjan kentät ovat pakollisia!", 400

        return redirect("/")

    reference_types = util.get_citation_styles()
    selected_style = request.args.get("style")
    return render_template(
        "add_reference.html",
        reference_types=reference_types,
        selected_style=selected_style,
    )


@app.route("/new_todo")
def new():
    return render_template("new_todo.html")


@app.route("/create_todo", methods=["POST"])
def todo_creation():
    content = request.form.get("content")

    try:
        validate_todo(content)
        create_todo(content)
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/new_todo")


@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})

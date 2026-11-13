from flask import flash, jsonify, redirect, render_template, request

import util
from config import app, test_env
from db_helper import reset_db
from repositories import citation_repository


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

        try:
            util.validate_reference(style_name, request.form)
        except util.UserInputError as error:
            return str(error), 400

        if style_name == "Kirja":
            citation_repository.create_book(
                request.form.get("citation_key"),
                request.form.get("author"),
                request.form.get("title"),
                request.form.get("year"),
                request.form.get("publisher"),
                style_name,
            )
        return redirect("/")

    reference_types = citation_repository.get_reference_types()
    selected_style = request.args.get("style")
    return render_template(
        "add_reference.html",
        reference_types=reference_types,
        selected_style=selected_style,
    )

@app.route("/references")
def show_references():
    references = citation_repository.get_all_citations()
    return render_template("sources.html", references=references)


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

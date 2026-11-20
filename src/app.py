from flask import jsonify, redirect, render_template, request

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
            if style_name == "Kirja":
                book = util.create_book_citation(request.form)
                util.validate_reference(book)
                citation_repository.save_book(book)
            else:
                raise util.UserInputError("Tuntematon viitetyyppi!")
        except util.UserInputError as error:
            return str(error), 400

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


@app.route("/references/<int:citation_id>")
def show_reference(citation_id):
    reference = citation_repository.get_citation_by_id(citation_id)

    if reference is None:
        return "Viitettä ei löytynyt.", 404

    return render_template("reference.html", reference=reference)


@app.route("/references/<int:citation_id>/delete", methods=["GET", "POST"])
def delete_reference(citation_id):
    reference = citation_repository.get_citation_by_id(citation_id)

    if reference is None:
        return "Viitettä ei löytynyt.", 404

    if request.method == "POST":
        citation_repository.delete_citation(citation_id)
        return redirect("/references")

    return render_template("delete_reference.html", reference=reference)


@app.route("/new_todo")
def new():
    return render_template("new_todo.html")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})

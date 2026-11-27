from flask import jsonify, redirect, render_template, request

import util
from bibtex import create_bibtex
from config import app, test_env
from db_helper import reset_db
from repositories import citation_repository


@app.route("/")
def index():
    author = request.args.get("author", "").strip()
    year_str = request.args.get("year", "").strip()

    year = None
    if year_str.isdigit():
        year = int(year_str)

    if author or year is not None:
        references = citation_repository.search_citations(
            author=author or None,
            year=year,
        )
    else:
        references = citation_repository.get_all_citations()

    return render_template(
        "index.html",
        references=references,
        search_author=author,
        search_year=year_str,
    )


@app.route("/add_reference", methods=["GET", "POST"])
def add_reference():
    if request.method == "POST":
        reference_type_name = request.form.get("reference_type_name")

        try:
            if reference_type_name == "book":
                book = util.create_book_citation(request.form)
                util.validate_reference(book)
                citation_repository.save_book(book)
            elif reference_type_name == "article":
                article = util.create_article_citation(request.form)
                util.validate_reference(article)
                citation_repository.save_article(article)
            elif reference_type_name == "inproceedings":
                inproceedings = util.create_inproceedings_citation(request.form)
                util.validate_reference(inproceedings)
                citation_repository.save_inproceedings(inproceedings)
            else:
                raise util.UserInputError("Tuntematon viitetyyppi!")
        except util.UserInputError as error:
            return str(error), 400

        return redirect("/")

    reference_types = citation_repository.get_reference_types()
    selected_type = request.args.get("reference_type_name")
    return render_template(
        "add_reference.html",
        reference_types=reference_types,
        selected_type=selected_type,
    )


@app.route(
    "/references/<int:citation_id>/edit_reference", methods=["GET", "POST"]
)
def edit_existing_reference(citation_id):
    reference = citation_repository.get_citation_by_id(citation_id)

    if reference is None:
        return "Viitettä ei löytynyt.", 404

    if request.method == "POST":
        reference_type_name = request.form.get("reference_type_name")

        try:
            if reference_type_name == "book":
                book = util.create_book_citation(request.form)
                util.validate_reference(book, exclude_citation_id=citation_id)
                citation_repository.update_book(citation_id, book)
            elif reference_type_name == "article":
                article = util.create_article_citation(request.form)
                util.validate_reference(
                    article, exclude_citation_id=citation_id
                )
                citation_repository.update_article(citation_id, article)
            elif reference_type_name == "inproceedings":
                inproceedings = util.create_inproceedings_citation(request.form)
                util.validate_reference(
                    inproceedings, exclude_citation_id=citation_id
                )
                citation_repository.update_inproceedings(
                    citation_id, inproceedings
                )
            else:
                raise util.UserInputError("Tuntematon viitetyyppi!")
        except util.UserInputError as error:
            return str(error), 400

        return redirect(f"/references/{citation_id}")

    reference_types = citation_repository.get_reference_types()
    return render_template(
        "edit_reference.html",
        reference_types=reference_types,
        selected_type=reference.reference_type_name,
        reference=reference,
    )


@app.route("/references/<int:citation_id>")
def show_reference(citation_id):
    reference = citation_repository.get_citation_by_id(citation_id)

    if reference is None:
        return "Viitettä ei löytynyt.", 404

    bibtex = create_bibtex(reference)
    return render_template("reference.html", reference=reference, bibtex=bibtex)


@app.route("/references/<int:citation_id>/delete", methods=["GET", "POST"])
def delete_reference(citation_id):
    reference = citation_repository.get_citation_by_id(citation_id)

    if reference is None:
        return "Viitettä ei löytynyt.", 404

    if request.method == "POST":
        citation_repository.delete_citation(citation_id)
        return redirect("/")

    return render_template("delete_reference.html", reference=reference)


@app.route("/download")
def download_references():
    references = citation_repository.get_all_citations()
    bibtex = [create_bibtex(ref) for ref in references]
    return render_template("download.html", bibtex=bibtex)


@app.route("/new_todo")
def new():
    return render_template("new_todo.html")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})

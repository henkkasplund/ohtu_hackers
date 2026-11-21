FIELDS = [
    "author",
    "title",
    "booktitle",
    "journal",
    "volume",
    "pages",
    "year",
    "publisher"
]


def create_bibtex(reference):
    lines = []
    for field in FIELDS:
        value = getattr(reference, field)
        if value:
            lines.append(f"  {field} = {{{value}}}")

    text = ",\n".join(lines)

    return f"@{reference.reference_type_name}{{{reference.citation_key},\n{text}\n}}"

class Citation:
    def __init__(
        self,
        citation_key,
        author,
        title,
        year,
        reference_type_name,
        citation_id=None,
        booktitle=None,
        journal=None,
        volume=None,
        pages=None,
        publisher=None,
        reference_type_display_name=None,
    ):
        self.citation_id = citation_id
        self.citation_key = citation_key
        self.author = author
        self.title = title
        self.year = year
        self.reference_type_name = reference_type_name
        self.booktitle = booktitle
        self.journal = journal
        self.volume = volume
        self.pages = pages
        self.publisher = publisher
        self.reference_type_display_name = reference_type_display_name

    def __str__(self):
        return f"{self.citation_key}: {self.author}, {self.title} ({self.year})"

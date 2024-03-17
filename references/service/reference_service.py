from ..models import Journal, Author, Reference


class ReferenceService:
    """
    Class that returns a reference dictionary ready to be serialized and saved. Utilises get or create to prevent duplicates.
    """

    def __init__(self, reference_data: dict):
        self.title = reference_data["title"]
        self.year = reference_data["year"]
        self.journal = reference_data["journal"]
        self.authors = reference_data["authors"]
        self.citation = reference_data["citation"]
        self.doi = reference_data["doi"]

    def _create_journal_instance(self):
        journal_instance, created = Journal.objects.get_or_create(
            journal_name=self.journal
        )
        self.journal = journal_instance.pk

    def _create_author_instances(self):
        author_list = []
        for author in self.authors:
            author_instance, created = Author.objects.get_or_create(name=author)
            author_list.append(author_instance.pk)
        self.authors = author_list

    def create_reference(self):
        self._create_journal_instance()
        self._create_author_instances()
        # Check for reference instance as well
        reference_instance, created = Reference.objects.get_or_create(
            title=self.title,
            year=self.year,
            journal=self.journal,
            authors=self.authors,
            citation=self.citation,
            doi=self.doi,
        )
        return reference_instance

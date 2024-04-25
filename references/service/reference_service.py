from ..models import Journal, Author, Reference


class ReferenceService:
    """
    Class that returns a reference dictionary ready to be serialized and saved. Utilises get or create to prevent duplicates.
    """

    def __init__(self, reference_data: dict):
        self.title = reference_data["title"]
        self.year = reference_data["year"]
        self.journal_name = reference_data["journal"]
        self.author_names = reference_data["authors"]
        self.citation = reference_data["citation"]
        self.doi = reference_data["doi"]

    def _create_journal_instance(self):
        journal_instance, created = Journal.objects.get_or_create(
            name=self.journal_name
        )
        return journal_instance

    def _create_author_instances(self):
        author_instances = []
        for author_name in self.author_names:
            author_instance, created = Author.objects.get_or_create(name=author_name)
            author_instances.append(author_instance)
        return author_instances

    def create_reference(self):
        journal_instance = self._create_journal_instance()
        author_instances = self._create_author_instances()

        # Create or get the reference
        reference_instance, created = Reference.objects.get_or_create(
            title=self.title,
            year=self.year,
            journal=journal_instance,
            citation=self.citation,
            doi=self.doi,
        )

        # Add authors to the reference (Many-to-Many relationship)
        reference_instance.authors.add(*author_instances)

        return reference_instance


def retrieve_references(references: list) -> list:
    # Return a list of primary keys of each instance for now
    reference_instances = []
    for reference in references:
        reference_service_object = ReferenceService(reference)
        reference_instance = reference_service_object.create_reference()
        reference_instances.append(reference_instance)
    return reference_instances

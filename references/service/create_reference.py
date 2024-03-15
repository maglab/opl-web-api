from ..models import Journal, Author, Reference
from get_doi_information import doi_crossref_search
from get_pmid_information import (
    PMIDRequestException,
    get_pmid_information,
    get_pmid_citation,
)


class ReferenceService:
    """
    Class that returns a reference dictionary ready to be serialized and saved.
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
        reference_instance = Reference(
            title=self.title,
            year=self.year,
            journal=self.journal,
            authors=self.authors,
            citation=self.citation,
            doi=self.doi,
        )
        reference_instance.save()
        return reference_instance


def create_reference(ref_type, value):
    if ref_type == "DOI":
        doi_information = doi_crossref_search(value)
        return doi_information

    elif ref_type == "PMID":
        # Get the reference information from pubmed api first and the retrieve the citation from the api.
        # Create single dictionary to use
        try:
            pmid_information = get_pmid_information(value)
        except ValueError as e:
            return e

        try:
            pmid_reference = get_pmid_citation(value)
        except PMIDRequestException:
            return PMIDRequestException

        if pmid_reference is not None and pmid_information is not None:
            return {
                "title": pmid_information["title"],
                "publish_date": pmid_information["year"],
                "journal": pmid_information["journal"],
                "citation": pmid_reference,
                "doi": pmid_information.get("doi"),
            }

    return None

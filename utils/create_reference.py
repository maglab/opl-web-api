from open_problems.models import Journal
from .get_doi_information import doi_crossref_search
from .get_pmid_information import (
    PMIDRequestException,
    get_pmid_information,
    get_pmid_citation,
)


def create_reference(ref_type, value):
    """
    Create a reference based on the given reference type and value.

    Args:
        ref_type (str): The type of reference ("DOI" or "PMID").
        value (str): The value associated with the reference type.

    Returns:
        dict or None: A dictionary containing reference information including title, year, journal, volume,
                     citation, and DOI. If the reference type is unsupported or no valid reference information
                     is found, returns None.
    """
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


def create_journal_instance(reference_dict: dict) -> dict:
    """
    Format reference_dict reference instance using dictionary of reference information. Needed only because journal is a foreign key
    and submitted journal data is a string.
    Args:
        reference_dict (dict): Dictionary of reference information
    Returns:
         dict - Returns the same dictionary but with changed journal value to an instance instead of journal title

    """
    journal_instance, created = Journal.objects.get_or_create(
        journal_name=reference_dict["journal"]
    )
    reference_dict["journal_id"] = journal_instance
    return {key: value for key, value in reference_dict.items() if key != "journal"}


def create_author_instances(reference_dict):
    ...

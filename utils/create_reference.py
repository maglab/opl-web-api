from .get_doi_information import doi_crossref_search
from .get_pmid_information import (
    PMIDRequestException,
    get_pmid_information,
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
        pmid_information, pmid_reference = None, None

        try:
            pmid_information = get_pmid_information(value)
        except ValueError:
            pass

        try:
            pmid_reference = get_pmid_citation(value)
        except PMIDRequestException:
            pass

        if pmid_reference is not None and pmid_information is not None:
            return {
                "title": pmid_information["title"],
                "year": pmid_information["year"],
                "journal": pmid_information["journal"],
                "citation": pmid_reference,
                "doi": pmid_information.get("doi"),
            }

    return None

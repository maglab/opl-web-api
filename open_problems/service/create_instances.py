from core.service import get_or_create_instance
from references.models import Author, Journal
from references.service import (
    PMIDRequestException,
    PmidConverter,
    DoiConverter,
)
from users.models import Contact, Organisation, JobField


def create_contact(data: dict):
    """
    Create a contact using post request data from the front end.
    Args:
        data: dict - Dictionary containing form values
    Returns:
        contact instance.
    """
    # Extract data
    organisation = data["organisation"]
    job_field = data["job_field"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if first_name and last_name or email:
        organisation_instance, created = (
            Organisation.objects.get_or_create(info_title=organisation)
            if organisation
            else None
        )
        job_field_instance, created = (
            JobField.objects.get_or_create(info_title=job_field) if job_field else None
        )
        contact_instance, created = Contact.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            job_field=job_field_instance,
            organisation=organisation_instance,
        )

        return contact_instance
    else:
        return None


def pmid_doi_conversion(reference_identifiers: list) -> tuple:
    # Currently only used by open problems -> will extend to other apps and move this into the core app.
    """
    Converts an array of PMID or DOIs into a dictionary of reference information.
    Args:
        reference_identifiers: list - An array of DOI or PMID. eg: [PMID:XXXXXXX, PMID:XXXXXX]
    Returns:
        Tuple of successfully converted references as reference instances and unsuccessfully converted references
    """
    converted_references = []
    unconverted_references = []
    # Split the string and return pmid or doi information
    # This string is validated by front-end so the split should always return two elements
    for identifier in reference_identifiers:
        id_type, value = identifier.split(":")
        try:
            if id_type.lower() == "doi":
                conversion = DoiConverter(
                    identifier=value, author=Author, journal=Journal
                )
            else:
                conversion = PmidConverter(
                    identifier=value, author=Author, journal=Journal
                )
            reference_information = conversion.retrieve_reference()
            reference_instance = get_or_create_instance(
                parameters=reference_information
            )
            converted_references.append(reference_instance.pk)
        except (PMIDRequestException, ValueError):
            unconverted_references.append(identifier)

    return converted_references, unconverted_references

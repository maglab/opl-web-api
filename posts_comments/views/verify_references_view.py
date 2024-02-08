import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.get_doi_information import doi_crossref_search
from utils.get_pmid_information import get_pmid_information


@api_view(["POST"])
def verify_reference(request):
    reference_type = request.data["type"]
    value = request.data["value"]

    if reference_type == "DOI":
        doi_information = doi_crossref_search(value)
        if not doi_information:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=doi_information, status=status.HTTP_200_OK)
    elif reference_type == "PMID":
        pmid_information = get_pmid_information(value)
        if not pmid_information:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=pmid_information, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_references(request):
    try:
        references = request.data["references"]
        verified_references = []
        unverified_references = []

        for reference in references:
            reference_type = reference["type"]
            value = reference["value"]
            if reference_type == "DOI":
                try:
                    doi_information = doi_crossref_search(value)
                    if not doi_information:
                        unverified_references.append(
                            {"type": "DOI", "value": value, "error": "Not found"}
                        )
                    else:
                        verified_references.append(doi_information)
                except AttributeError:
                    unverified_references.append(
                        {"type": "DOI", "value": value, "error": "Not found"}
                    )

            elif reference_type == "PMID":
                try:
                    pmid_information = get_pmid_information(value)
                except ValueError:
                    unverified_references.append(
                        {"type": "PMID", "value": value, "error": "Not found"}
                    )
                else:
                    if not pmid_information:
                        unverified_references.append(
                            {"type": "PMID", "value": value, "error": "Not found"}
                        )
                    else:
                        verified_references.append(pmid_information)

        return Response(
            data={
                "verified_references": verified_references,
                "unverified_references": unverified_references,
            },
            status=status.HTTP_200_OK,
        )
    except json.JSONDecodeError:
        return Response(
            data={"error": "Invalid JSON data in the request body"},
            status=status.HTTP_400_BAD_REQUEST,
        )

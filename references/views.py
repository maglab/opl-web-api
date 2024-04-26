from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .service import (
    PmidConverter,
    DoiConverter,
    PMIDRequestException,
    DOIRequestException,
)


@api_view(["POST"])
def convert_reference(request):
    reference_type = request.data["type"]
    value = request.data["value"]

    if reference_type == "DOI":
        try:
            doi_converter = DoiConverter(value)
            doi_information = doi_converter.retrieve_reference()
            if not doi_information:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except DOIRequestException:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=doi_information, status=status.HTTP_200_OK)
    elif reference_type == "PMID":
        try:
            pmid_converter = PmidConverter(value)
            pmid_information = pmid_converter.retrieve_reference()
            if not pmid_information:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except PMIDRequestException:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=pmid_information, status=status.HTTP_200_OK)

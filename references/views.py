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
    try:
        reference_type = request.data["type"]
        value = request.data["value"]
        if reference_type == "DOI":
            converter_object = DoiConverter(identifier=value)
        elif reference_type == "PMID":
            converter_object = PmidConverter(identifier=value)
        else:
            return Response(
                data={"error": "Incorrect reference type. Must be DOI or PMID."}
            )

        try:
            reference_data = converter_object.retrieve_reference()
            return Response(data={"reference": reference_data})
        except (DOIRequestException, PMIDRequestException) as e:
            return Response(data={"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return Response(
            data={"error": "Incorrect format for endpoint"},
            status=status.HTTP_400_BAD_REQUEST,
        )

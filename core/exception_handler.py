from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


def custom_exception_handler(exc, ctx):
    """
    Standardized error response format:
    {
        "message": "Error message",
        "extra": {}
    }
    """
    # Convert Django-specific validation error to DRF validation error
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    # Convert Django's Http404 to DRF's NotFound exception
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    # Convert Django's PermissionDenied to DRF's PermissionDenied exception
    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    # Let DRF handle the exception first
    response = exception_handler(exc, ctx)

    # Handle unexpected errors (e.g., custom ApplicationError)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {"message": exc.message, "extra": exc.extra}
            return Response(data, status=400)

        # For other unhandled exceptions, leave the default behavior
        return response

    # Wrap detailed errors into a standardized format
    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    # Handle specific error types to provide more context
    if isinstance(exc, exceptions.ParseError):
        print("running")
        response.data["message"] = response.data.get(
            "message", "Unwanted fields sent to endpoint"
        )
        response.data["extra"] = response.data.get("extra", {})

    elif isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {"fields": response.data["detail"]}

    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response

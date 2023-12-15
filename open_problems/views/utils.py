from django.http import JsonResponse
from requests import post
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils.token_required import token_login_required


@api_view(["POST"])
def verify_token(request):
    """Verify google recaptcha token"""
    if request.method == "POST":
        data = request.data
        post_request = post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": data["secret"], "response": data["response"]},
        )
        content = post_request.text
        return Response(content)


@api_view(["GET"])
@token_login_required
def test_view(request):
    # If the middleware is working correctly, request.user should be set to the authenticated user
    user = request.user
    return JsonResponse(
        {
            "username": user.username,
            "email": user.email,
            "is_authenticated": user.is_authenticated,
        }
    )

from rest_framework.decorators import api_view
from rest_framework.response import Response
from requests import post


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


def parse_submitted_references(data):
    """Parse submitted references from JSON"""

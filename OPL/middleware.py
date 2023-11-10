import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from jwt import ExpiredSignatureError, InvalidTokenError

User = get_user_model()


class AzureADTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization", "").split()
        token = (
            auth_header[1]
            if len(auth_header) == 2 and auth_header[0].lower() == "bearer"
            else None
        )

        if token:
            try:
                decoded_token = self.validate_token(token)
                self.authenticate_request(request, decoded_token)
            except ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except InvalidTokenError as e:
                return JsonResponse({"error": str(e)}, status=401)
            except Exception as e:
                return JsonResponse({"error": "Invalid token"}, status=401)

        response = self.get_response(request)
        return response

    @staticmethod
    def validate_token(token):
        jwks_client = jwt.PyJWKClient(
            f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/discovery/v2.0/keys"
        )
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # Decode and validate the JWT
        decoded_token = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.AZURE_CLIENT_ID,
            issuer=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}/v2.0",
        )
        return decoded_token

    @staticmethod
    def authenticate_request(request, decoded_token):
        # Assuming the token contains the user's email in 'upn' or 'email' claim
        user_email = decoded_token.get("upn") or decoded_token.get("email")
        user, _ = User.objects.get_or_create(email=user_email)
        request.user = user

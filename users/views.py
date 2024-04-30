from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

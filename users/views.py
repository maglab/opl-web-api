from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from core.service.mailer import EmailSenderTemplate


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    email_template_id = "7dnvo4ddxxn45r86"

    def prepare_email(self, instance):
        first_name = instance.first_name
        last_name = instance.last_name
        full_name = f"{first_name} {last_name}"
        email = instance.email
        recipients = {"name": full_name, "email": email}
        mail_from = {"name": "Angelo", "domain": ""}
        personalization = {"email": email, "data": {"name": full_name}}
        mailer_instance = EmailSenderTemplate(
            subject="Hello from Open Longevity",
            template_id=self.email_template_id,
            recipients=recipients,
            mail_from=mail_from,
            personalization=personalization,
        )
        return mailer_instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            prepared_email = self.prepare_email(instance)
            prepared_email.send_email()
        return Response(status=status.HTTP_201_CREATED)

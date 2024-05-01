import os
from unittest import TestCase

from django.core.mail import EmailMessage
from django.conf import settings


class EmailTestCase(TestCase):
    def setUp(self):
        settings.EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        settings.EMAIL_HOST = "sandbox.smtp.mailtrap.io"
        settings.EMAIL_HOST_USER = os.environ.get("EMAIL_TEST_HOST_USER")
        settings.EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_TEST_HOST_PASSWORD")
        settings.EMAIL_PORT = "2525"

    @staticmethod
    def test_send_email():
        subject = "That’s your subject"
        plain_message = "Test body"
        from_email = "from@yourdjangoapp.com"
        to = "to@yourbestuser.com"

        message = EmailMessage(
            subject=subject, body=plain_message, from_email=from_email, to=(to,)
        )

        message.send()

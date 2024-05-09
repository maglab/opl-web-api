import json
import os
from abc import ABC, abstractmethod
import mailtrap
from django.conf import settings


class ClientConfigurator(ABC):
    @abstractmethod
    def configure_client(self):
        pass


class MailtrapConfigurator(ClientConfigurator):
    DEFAULT_HOST = mailtrap.MailtrapClient.DEFAULT_HOST
    DEFAULT_PORT = mailtrap.MailtrapClient.DEFAULT_PORT

    def __init__(
        self, token: str, api_host: str = DEFAULT_HOST, api_port: int = DEFAULT_PORT
    ):
        self.token = token
        self.api_host = api_host
        self.api_port = api_port

    def configure_client(self):
        return mailtrap.MailtrapClient(
            token=self.token, api_host=self.api_host, api_port=self.api_port
        )


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, to_email, subject, body, name):
        pass


class MailtrapTemplateEmailSender(EmailSender):
    sender = os.environ.get("MAILTRAP_SENDER")

    def __init__(self, client: mailtrap.MailtrapClient):
        self.client = client

    def send_email(
        self,
        to_email: str,
        template_uuid: str,
        template_variables: dict,
        name: str = "Open Longevity Group",
    ):
        mail = mailtrap.MailFromTemplate(
            sender=mailtrap.Address(email=self.sender, name=name),
            to=[mailtrap.Address(email=to_email)],
            template_uuid=template_uuid,
            template_variables=template_variables,
        )
        self.client.send(mail)


# Classes for extracting template variables
class Extractor(ABC):
    @staticmethod
    @abstractmethod
    def extract(data):
        pass


class EmailExtractor(Extractor):

    @staticmethod
    def extract(data):
        email = data.get("email", "")
        if email:
            receiver = email.split("@")[0]
            return receiver, email
        return None


def get_templates(file_path: str = "core/emails/uuid_config.json") -> dict:
    base_dir = settings.BASE_DIR
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, mode="r") as file:  # This might be incorrect
        templates = json.load(file)
    return templates

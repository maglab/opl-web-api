import os
import mailtrap
from abc import ABC, abstractmethod

TEMPLATE_MAPPING = {"submit_problem_confirmation": ""}


def set_up_mailtrap_client(
    api_host: str = mailtrap.MailtrapClient.DEFAULT_HOST,
    api_port: int = mailtrap.MailtrapClient.DEFAULT_PORT,
) -> mailtrap.MailtrapClient:
    api_key = os.environ.get("MAILTRAP_API_KEY")
    client = mailtrap.MailtrapClient(
        token=api_key, api_port=api_port, api_host=api_host
    )
    return client


class MailTrapSender:
    sender = os.environ.get("MAILTRAP_SENDER")

    def __init__(self, client: mailtrap.MailtrapClient) -> None:
        self.client = client

    def send_template_email(
        self, uuid: str, variables: dict, to_email: str, name: str
    ) -> None:
        template = mailtrap.MailFromTemplate(
            sender=mailtrap.Address(email=self.sender, name=name),
            to=[mailtrap.Address(to_email)],
            template_uuid=uuid,
            template_variables=variables,
        )
        self.client.send(template)


# Classes for extracting template variables
class Extractor(ABC):
    @abstractmethod
    def extract(self, data):
        pass


class EmailExtractor(Extractor):
    def extract(self, data):
        email = data.get("email", "")
        if email:
            receiver = email.split("@")[0]
            return receiver
        return email

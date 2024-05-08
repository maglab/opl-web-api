from abc import ABC, abstractmethod
import mailtrap


class ClientConfigurator(ABC):
    @abstractmethod
    def configure_client(self):
        pass


class MailtrapConfigurator(ClientConfigurator):
    DEFAULT_HOST = "api.mailtrap.io"
    DEFAULT_PORT = 2525

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


class EmailClientFactory:
    def __init__(self, client_configurator: ClientConfigurator):
        self.client_configurator = client_configurator

    def get_configured_client(self) -> ClientConfigurator.configure_client:
        client = self.client_configurator.configure_client()
        return client


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, to_email, subject, body):
        pass


class MailtrapTemplateEmailSender(EmailSender):
    def __init__(self, client: mailtrap.MailtrapClient):
        self.client = client

    def send_email(self, to_email: str, template_uuid: str, template_variables: dict):
        mail = mailtrap.MailFromTemplate(
            sender=mailtrap.Address(
                email="mailtrap@longevityknowledge.app", name="Mailtrap Test"
            ),
            to=[mailtrap.Address(email="openlongevitydevgroup@gmail.com")],
            template_uuid="f284b412-5513-41fd-beb5-5b2da5f86f65",
            template_variables=template_variables,
        )
        self.client.send(mail)


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

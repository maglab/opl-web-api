import os
import mailtrap


class MailTrapService:
    client = mailtrap.MailtrapClient(token=os.environ.get("MAILTRAP_API_KEY"))
    sender = os.environ.get("MAILTRAP_SENDER")

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

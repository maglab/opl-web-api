from mailersend import emails
import os


class EmptyEmailBodyError(Exception):
    """Exception raised when user has not set up the email body"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)


class EmailSenderTemplate:
    mail_body = {}
    mailer = emails.NewEmail(os.environ.get("MAILERSEND_API_KEY"))
    ready_to_send = False

    def __init__(
        self,
        subject: str,
        template_id: str,
        mail_from: dict,
        recipients: dict,
        personalization: dict,
    ):
        self.subject = subject
        self.template_id = template_id
        self.mail_from = mail_from
        self.recipients = recipients
        self.personalization = personalization

    def set_up_email(self):
        self.mailer.set_mail_from(self.mail_from, self.mail_body)
        self.mailer.set_mail_to(self.recipients, self.mail_body)
        self.mailer.set_subject(self.subject, self.mail_body)
        self.mailer.set_template(self.template_id, self.mail_body)
        self.mailer.set_advanced_personalization(self.personalization, self.mail_body)
        self.ready_to_send = True

    def send_email(self):
        if self.ready_to_send:
            self.mailer.send(self.mail_body)
        else:
            raise EmptyEmailBodyError(
                "Please set up the email body through set_up_emal()"
            )

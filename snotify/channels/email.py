from typing import List, Union
import aiosmtplib
from email.message import EmailMessage
from .base import BaseChannel, BaseRecipient
import logging


class EmailRecipientTypeError(TypeError):
    """Custom exception for invalid recipient types."""

    pass


class EmailChannel(BaseChannel):
    """
    A class for sending notifications via email using SMTP.

    This class allows you to configure an SMTP server and send email notifications to a list of recipients.

    Parameters
    ----------
    smtp_server : str
        The address of the SMTP server.
    smtp_port : int
        The port number of the SMTP server.
    smtp_user : str
        The username for SMTP authentication.
    smtp_password : str
        The password for SMTP authentication.
    recipients : Union[List[BaseRecipient], List[str]]
        A list of recipient objects implementing the BaseRecipient interface or email addresses in str format.

    Methods
    -------
    send(message: str, subject: str = "Notification", recipients: List[BaseRecipient] = None)
        Sends an email message to the specified recipients.
    validate_config()
        Validates the SMTP configuration.
    """

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        recipients: Union[List[BaseRecipient], List[str]],
    ):
        super().__init__(recipients)
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    async def send(
        self,
        message: str,
        subject: str = "Notification",
        recipients: List[BaseRecipient] = None,
    ):
        logger = logging.getLogger(__name__)
        recipients_to_use = recipients if recipients is not None else self.recipients

        for recipient in recipients_to_use:
            if isinstance(recipient, str):
                recipient = EmailRecipient(name=recipient, email=recipient)

            email = EmailMessage()
            email["From"] = self.smtp_user
            email["To"] = recipient.get_recipient_id()
            email["Subject"] = subject
            email.set_content(message)

            try:
                await aiosmtplib.send(
                    email,
                    hostname=self.smtp_server,
                    port=self.smtp_port,
                    username=self.smtp_user,
                    password=self.smtp_password,
                )
                logger.info(
                    f"✅ Sent email to {recipient.get_recipient_name()} ({recipient.get_recipient_id()})"
                )
            except Exception as e:
                error_msg = f"Failed to send email to {recipient.get_recipient_name()}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                raise RuntimeError(error_msg)

    def validate_config(self):
        if not all(
            [self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_password]
        ):
            raise ValueError("SMTP configuration is incomplete")
        for recipient in self.recipients:
            if not isinstance(recipient, EmailRecipient) and not isinstance(
                recipient, str
            ):
                raise EmailRecipientTypeError(
                    f"The {recipient} recipient must be either str or EmailRecipient"
                )


class EmailRecipient(BaseRecipient):
    """
    A class representing an email recipient.

    This class stores the recipient's name and email address and provides methods to retrieve them.

    Parameters
    ----------
    name : str
        The name of the recipient.
    email : str
        The email address of the recipient.

    Methods
    -------
    get_recipient_id() -> str
        Returns the recipient's email address.
    get_recipient_name() -> str
        Returns the recipient's name.
    """

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def get_recipient_id(self) -> str:
        return self.email

    def get_recipient_name(self) -> str:
        return self.name

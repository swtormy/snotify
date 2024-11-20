from typing import List
import aiohttp
from .base import BaseChannel, BaseRecipient
import logging


class WebhookChannel(BaseChannel):
    """
    A class for sending notifications via Webhook.

    This class allows you to configure a Webhook URL and send messages to it.

    Parameters
    ----------
    webhook_url : str
        The URL of the Webhook.
    recipients : List[BaseRecipient]
        A list of recipient objects implementing the BaseRecipient interface.

    Methods
    -------
    send(message: str, recipients: List[BaseRecipient] = None)
        Sends a message to the specified Webhook.
    validate_config()
        Validates the Webhook URL.
    """

    def __init__(self, webhook_url: str, recipients: List[BaseRecipient]):
        super().__init__(recipients)
        self.webhook_url = webhook_url

    async def send(self, message: str, recipients: List[BaseRecipient] = None):
        logger = logging.getLogger(__name__)
        recipients_to_use = recipients if recipients is not None else self.recipients
        for recipient in recipients_to_use:
            payload = {"recipient": recipient.get_recipient_id(), "message": message}

            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"✅ Sent to {recipient.get_recipient_name()}")
                    else:
                        error_msg = f"Failed to send to {recipient.get_recipient_name()}: {await response.text()}"
                        logger.error(f"❌ {error_msg}")
                        raise RuntimeError(error_msg)

    def validate_config(self):
        if not self.webhook_url:
            raise ValueError("Webhook URL is required")


class WebhookRecipient(BaseRecipient):
    """
    A class representing a Webhook recipient.

    This class stores the recipient's name and identifier (e.g., a unique key or ID for the Webhook) and provides methods to retrieve them.

    Parameters
    ----------
    name : str
        The name of the recipient.
    identifier : str
        The unique identifier for the Webhook recipient.

    Methods
    -------
    get_recipient_id() -> str
        Returns the recipient's identifier.
    get_recipient_name() -> str
        Returns the recipient's name.
    """

    def __init__(self, name: str, identifier: str):
        self.name = name
        self.identifier = identifier

    def get_recipient_id(self) -> str:
        return self.identifier

    def get_recipient_name(self) -> str:
        return self.name

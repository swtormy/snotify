from typing import List
import aiohttp
from .base import BaseChannel, BaseRecipient
import logging

class TelegramChannel(BaseChannel):
    """
    A class for sending notifications via Telegram using a bot.

    This class allows you to configure a Telegram bot and send messages to a list of recipients.

    Parameters
    ----------
    bot_token : str
        The token of the Telegram bot.
    recipients : List[BaseRecipient]
        A list of recipient objects implementing the BaseRecipient interface.

    Methods
    -------
    send(message: str, recipients: List[BaseRecipient] = None)
        Sends a message to the specified recipients.
    validate_config()
        Validates the bot token and recipients list.
    """
    def __init__(self, bot_token: str, recipients: List[BaseRecipient]):
        super().__init__(recipients)
        self.bot_token = bot_token

    async def send(self, message: str, recipients: List[BaseRecipient] = None):
        logger = logging.getLogger(__name__)
        recipients_to_use = recipients if recipients is not None else self.recipients
        for recipient in recipients_to_use:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": recipient.get_recipient_id(), "text": message}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"✅ Sent to {recipient.get_recipient_name()}")
                    else:
                        error_msg = f"Failed to send to {recipient.get_recipient_name()}: {await response.text()}"
                        logger.error(f"❌ {error_msg}")
                        raise RuntimeError(error_msg)

    def validate_config(self):
        if not self.bot_token:
            raise ValueError("Telegram bot_token is required")
        if not self.recipients:
            raise ValueError("Telegram recipients are required")


class TelegramRecipient(BaseRecipient):
    """
    A class representing a Telegram recipient.

    This class stores the recipient's name and chat ID and provides methods to retrieve them.

    Parameters
    ----------
    name : str
        The name of the recipient.
    chat_id : str
        The chat ID of the recipient.

    Methods
    -------
    get_recipient_id() -> str
        Returns the recipient's chat ID.
    get_recipient_name() -> str
        Returns the recipient's name.
    """
    def __init__(self, name: str, chat_id: str):
        self.name = name
        self.chat_id = chat_id

    def get_recipient_id(self) -> str:
        return self.chat_id

    def get_recipient_name(self) -> str:
        return self.name
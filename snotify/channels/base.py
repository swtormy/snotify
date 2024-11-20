from typing import List
from abc import ABC, abstractmethod


class BaseRecipient(ABC):
    """
    An interface defining the structure of a recipient.

    Methods
    -------
    get_recipient_id() -> str
        Returns the recipient's identifier (e.g., email or chat_id).
    get_recipient_name() -> str
        Returns the recipient's name.
    """

    @abstractmethod
    def get_recipient_id(self) -> str:
        pass

    @abstractmethod
    def get_recipient_name(self) -> str:
        pass


class BaseChannel(ABC):
    """
    An abstract base class for notification channels.

    Parameters
    ----------
    recipients : List[BaseRecipient]
        A list of recipient objects implementing the BaseRecipient interface.

    Methods
    -------
    send(message: str, recipients: List[BaseRecipient] = None)
        Sends a notification message.
    validate_config()
        Validates the channel's configuration.
    """

    def __init__(self, recipients: List[BaseRecipient]):
        self.recipients = recipients

    @abstractmethod
    async def send(self, message: str, recipients: List[BaseRecipient] = None):
        pass

    @abstractmethod
    def validate_config(self):
        pass

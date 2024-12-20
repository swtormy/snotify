import logging
from typing import List
from .channels.base import BaseChannel, BaseRecipient


def configure_logging(level=logging.INFO):
    """
    Configures logging for the entire snotify library.

    Parameters
    ----------
    level : int
        The logging level (e.g., logging.DEBUG, logging.INFO).

    Usage
    -----
    To enable logging:
    >>> configure_logging(logging.DEBUG)

    To disable logging:
    >>> logging.disable(logging.CRITICAL)
    """
    logging.basicConfig(level=level)
    logging.getLogger("snotify.channels.email").setLevel(level)
    logging.getLogger("snotify.channels.telegram").setLevel(level)
    logging.getLogger("snotify.channels.webhook").setLevel(level)
    logging.getLogger("snotify.core").setLevel(level)


class Notifier:
    """
    A class that manages notification channels and handles message delivery with a fallback mechanism.

    This class allows you to add multiple notification channels and define a fallback order for message delivery.
    If a message fails to send through one channel, it will attempt to send through the next channel in the order.
    If no fallback order is set, the message will be sent to all channels.

    Methods
    -------
    add_channel(channel: BaseChannel, name: str)
        Adds a notification channel to the manager.
    set_fallback_order(order: List[str])
        Sets the order of channels to use in case of a failure. If not set, messages are sent to all channels.
    async send(message: str, recipients: List[BaseRecipient] = None)
        Sends a notification using the specified channels.

    Parameters
    ----------
    None

    Example
    -------
    >>> notifier = Notifier()
    >>> email_channel = EmailChannel(smtp_server, smtp_port, smtp_user, smtp_password, recipients)
    >>> notifier.add_channel(email_channel, "email")
    >>> notifier.set_fallback_order(["email", "telegram"])  # Optional
    >>> await notifier.send("Hello, World!")
    """

    def __init__(self):
        self.channels = []
        self.fallback_order = []

    def add_channel(self, channel: BaseChannel, name: str = None):
        """
        Adds a notification channel to the manager.
        :param channel: A channel implementing BaseChannel.
        :param name: Optional name of the channel for use in fallback_order.
                    If not provided, will be auto-generated from channel class name.
        """
        channel.validate_config()
        if name is None:
            base_name = channel.__class__.__name__.lower().replace("channel", "")
            similar_channels = [
                ch for ch in self.channels if ch["name"].startswith(base_name)
            ]

            if not similar_channels:
                name = base_name
            else:
                name = f"{base_name}_{len(similar_channels)}"

        self.channels.append({"name": name, "channel": channel})

    def set_fallback_order(self, order: List[str]):
        """
        Sets the order of channels to use in case of a failure.
        :param order: A list of channel names.
        """
        self.fallback_order = order

    async def send(self, message: str, recipients: List[BaseRecipient] = None):
        """
        Sends a notification using the specified channels.
        :param message: The message to send.
        :param recipients: A list of recipients implementing RecipientInterface. If not specified, channel recipients are used.
        """
        logger = logging.getLogger(__name__)

        if not self.fallback_order:
            logger.info("Fallback order is not set. Sending to all channels.")
            for channel_data in self.channels:
                channel = channel_data["channel"]
                try:
                    await channel.send(
                        message=message, recipients=recipients or channel.recipients
                    )
                    logger.info(
                        f"Message sent successfully via {channel_data['name']}."
                    )
                except Exception:
                    raise
        else:
            for name in self.fallback_order:
                channel_data = next(
                    (ch for ch in self.channels if ch["name"] == name), None
                )
                if not channel_data:
                    logger.warning(f"Channel {name} not found in added channels.")
                    continue

                channel = channel_data["channel"]
                try:
                    await channel.send(
                        message=message, recipients=recipients or channel.recipients
                    )
                    logger.info(f"Message sent successfully via {name}.")
                    break
                except Exception as e:
                    logger.error(f"Failed to send message via {name}: {e}")
            else:
                raise RuntimeError("All notification channels failed.")

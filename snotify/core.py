import logging
from typing import List
from .channels.base import BaseChannel, BaseRecipient
import asyncio
from concurrent.futures import ThreadPoolExecutor


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
    Synchronous notification manager that provides a blocking interface to send notifications.
    This is a wrapper around ANotifier that makes asynchronous operations appear synchronous.

    Example
    -------
    >>> notifier = Notifier()
    >>> notifier.add_channel(telegram_channel)
    >>> notifier.send("Hello World")  # Blocks until the message is sent

    Methods
    -------
    add_channel(channel: BaseChannel, name: str = None)
        Adds a notification channel to the manager.
    set_fallback_order(order: List[str])
        Sets the order of channels to use in case of a failure.
    send(message: str, recipients: List[BaseRecipient] = None)
        Sends a notification synchronously using the specified channels.
    """

    def __init__(self):
        self.channels = []
        self.fallback_order = []
        self._executor = ThreadPoolExecutor()

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

    def send(self, message: str, recipients: List[BaseRecipient] = None):
        """
        Sends a notification using the specified channels synchronously.
        :param message: The message to send.
        :param recipients: A list of recipients implementing RecipientInterface.
        """

        async def _async_send():
            async_notifier = ANotifier()
            async_notifier.channels = self.channels
            async_notifier.fallback_order = self.fallback_order
            await async_notifier.send(message, recipients)

        asyncio.run(_async_send())

    def __del__(self):
        self._executor.shutdown(wait=False)


class ANotifier:
    """
    Asynchronous notification manager that provides non-blocking interface to send notifications.
    This is the base implementation that handles actual message delivery.

    Example
    -------
    >>> async def main():
    >>>     notifier = ANotifier()
    >>>     notifier.add_channel(telegram_channel)
    >>>     await notifier.send("Hello World")
    >>>
    >>> asyncio.run(main())

    Methods
    -------
    add_channel(channel: BaseChannel, name: str = None)
        Adds a notification channel to the manager.
    set_fallback_order(order: List[str])
        Sets the order of channels to use in case of a failure.
    async send(message: str, recipients: List[BaseRecipient] = None)
        Sends a notification asynchronously using the specified channels.
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
        Sends a notification using the specified channels asynchronously.
        :param message: The message to send.
        :param recipients: A list of recipients implementing RecipientInterface.
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

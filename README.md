# snotify

Lightweight notification manager with support for Telegram, email, and custom channels.

## Description

`snotify` is a library for managing notifications that allows sending messages through various channels such as Telegram, email, and custom channels. It supports a fallback mechanism that allows sending messages through alternative channels in case the primary one fails.

## Installation

Install the library using pip:

```bash
pip install snotify
```

## Usage Example

```python
from snotify import Notifier, TelegramChannel, EmailChannel

# Create an instance of Notifier
notifier = Notifier()

# Add a Telegram channel
telegram_channel = TelegramChannel(bot_token="your_bot_token", recipients=[...])
notifier.add_channel(telegram_channel, "telegram")

# Add an Email channel
email_channel = EmailChannel(
    smtp_server="smtp.example.com",
    smtp_port=587,
    smtp_user="your_user",
    smtp_password="your_password",
    recipients=[...]
)
notifier.add_channel(email_channel, "email")

# Send a notification
await notifier.send("Your message")
```

## Creating a Custom Channel

To create a custom channel, you need to extend the `BaseChannel` class and implement the `send` and `validate_config` methods. Here's a basic example:

```python
from snotify.channels.base import BaseChannel, BaseRecipient
import logging

class CustomChannel(BaseChannel):
    def __init__(self, custom_param, recipients):
        super().__init__(recipients)
        self.custom_param = custom_param

    async def send(self, message, recipients=None):
        logger = logging.getLogger(__name__)
        recipients_to_use = recipients if recipients is not None else self.recipients
        for recipient in recipients_to_use:
            # Implement your custom sending logic here
            logger.info(f"Sending message to {recipient.get_recipient_name()} via custom channel")

    def validate_config(self):
        if not self.custom_param:
            raise ValueError("Custom parameter is required")
```

## Features

- **Support for multiple channels**: Telegram, Email, and Custom channels.
- **Fallback mechanism**: ability to specify the order of channels for sending messages in case of failure.
- **Easy setup and use**.

## Requirements

- Python 3.7+
- aiohttp
- aiosmtplib

## License

MIT License. See the LICENSE file for details.

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

### Basic Usage

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
    recipients=[...]  # Can be a list of strings or EmailRecipient objects
)
notifier.add_channel(email_channel, "email")

# Send a notification
await notifier.send("Your message")
```

### Using Fallback Mechanism

```python
# Set fallback order
notifier.set_fallback_order(["telegram", "email"])

# Send a notification with fallback
await notifier.send("Your message with fallback")
# Note: Errors are logged instead of raised when fallback is enabled
```

### Creating and Using a Custom Channel

To create a custom channel, you need to extend the `BaseChannel` class and implement the `send` and `validate_config` methods. Here's a basic example:

```python
from snotify.channels.base import BaseChannel, BaseRecipient
import logging

class CustomRecipientTypeError(TypeError):
    """Custom exception for invalid recipient types."""
    pass

class CustomChannel(BaseChannel):
    def __init__(self, custom_param, recipients):
        super().__init__(recipients)
        self.custom_param = custom_param

    async def send(self, message, recipients=None):
        logger = logging.getLogger(__name__)
        recipients_to_use = recipients if recipients is not None else self.recipients
        for recipient in recipients_to_use:
            if isinstance(recipient, str):
                recipient = CustomRecipient(name=recipient, chat_id=recipient)
            # Implement your custom sending logic here
            logger.info(f"Sending message to {recipient.get_recipient_name()} via custom channel")

    def validate_config(self):
        if not self.custom_param:
            raise ValueError("Custom parameter is required")
        for recipient in self.recipients:
            if not isinstance(recipient, CustomRecipient) and not isinstance(
                recipient, str
            ):
                raise CustomRecipientTypeError(
                    f"The {
                        recipient} recipient must be either str or CustomRecipient"
                )

# Add a custom channel
custom_channel = CustomChannel(custom_param="value", recipients=[...])
notifier.add_channel(custom_channel, "custom")

# Send a notification using the custom channel
await notifier.send("Your custom message")
```

## Features

- **Support for multiple channels**: Telegram, Email, and Custom channels.
- **Fallback mechanism**: ability to specify the order of channels for sending messages in case of failure. Errors are logged instead of raised when fallback is enabled.
- **Easy setup and use**.

## Requirements

To use `snotify`, you need the following Python packages:

- **Runtime Requirements**: These are the packages required to run the library.
  - `aiohttp>=3.7.4`: Asynchronous HTTP client/server framework.
  - `aiosmtplib>=1.1.6`: Asynchronous SMTP client for sending emails.

- **Development Requirements**: These are additional packages needed for development and testing.
  - `pre-commit>=2.13.0`: A framework for managing and maintaining multi-language pre-commit hooks.
  - `pytest>=6.2.4`: A framework that makes building simple and scalable test cases easy.
  - `pytest-asyncio>=0.14.0`: A `pytest` plugin for testing asyncio code.
  - `python-dotenv>=0.17.0`: Reads key-value pairs from a `.env` file and can set them as environment variables.
  - `setuptools>=52.0.0`: A package development and distribution library.

These dependencies are listed in the `requirements.txt` and `requirements-dev.txt` files, respectively. You can install them using pip:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## License

MIT License. See the LICENSE file for details.

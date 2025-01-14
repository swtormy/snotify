# snotify

Lightweight notification manager with support for Telegram, email, and custom channels. Supports both synchronous and asynchronous operations.

## Description

`snotify` is a library for managing notifications that allows sending messages through various channels such as Telegram, email, and custom channels. It supports both synchronous and asynchronous operations, and includes a fallback mechanism that allows sending messages through alternative channels in case the primary one fails.

#### Supported Notification Channels:

##### snotify currently supports the following channels:

`Telegram`: Instantly send messages to users via the Telegram platform.

`Email`: Deliver notifications directly to users' inboxes.

`Webhook`: Integrate with external systems by sending event data to specified URLs in real time.

`Custom Channels`: Extend functionality by creating and configuring your own notification channels.

## Installation

Install the library using pip:

```bash
pip install snotify
```


## Usage Example

### Configuring Logging

```python
from snotify import configure_logging
import logging

# Enable debug logging
configure_logging(logging.DEBUG)

# Or use INFO level (default)
configure_logging(logging.INFO)

# To disable logging completely
logging.disable(logging.CRITICAL)
```

### Synchronous Usage

```python
from snotify import Notifier, TelegramChannel, EmailChannel

# Create an instance of synchronous Notifier
notifier = Notifier()

# Add a Telegram channel
telegram_channel = TelegramChannel(bot_token="your_bot_token", recipients=["1234567890"])
notifier.add_channel(telegram_channel)

# Send a notification synchronously
notifier.send("Your message")  # This will block until the message is sent
```

### Asynchronous Usage

```python
from snotify import ANotifier, TelegramChannel, EmailChannel
import asyncio

async def send_notification():
    # Create an instance of asynchronous Notifier
    notifier = ANotifier()

    # Add a Telegram channel
    telegram_channel = TelegramChannel(bot_token="your_bot_token", recipients=["1234567890"])
    notifier.add_channel(telegram_channel)

    # Send a notification asynchronously
    await notifier.send("Your message")

# Run the async function
asyncio.run(send_notification())
```

### Using Fallback Mechanism (works in both sync and async modes)

```python
# Add an Email channel
email_channel = EmailChannel(
    smtp_server="smtp.example.com",
    smtp_port=587,
    smtp_user="your_user",
    smtp_password="your_password",
    recipients=['test@example.com']
)
notifier.add_channel(email_channel)

# Set fallback order
notifier.set_fallback_order(["telegram", "email"])

# Send a notification with fallback
notifier.send("Your message with fallback")  # For synchronous usage
# or
await notifier.send("Your message with fallback")  # For asynchronous usage
```

### Webhook Usage

```python
from snotify import Notifier, WebhookChannel

# Create an instance of synchronous Notifier
notifier = Notifier()

# Add a WebhookChannel channel
webhook_channel = WebhookChannel(
webhook_url="https://example.com/webhook",
recipients=["recipient1", "recipient2"]
)
notifier.add_channel(webhook_channel)

# Send a notification synchronously
notifier.send("Your message via Webhook")
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
notifier.add_channel(custom_channel)

# Send a notification using the custom channel
await notifier.send("Your custom message")
```

## Features

- **Flexible operation modes**: Support for both synchronous and asynchronous operations
- **Support for multiple channels**: Telegram, Email, and Custom channels
- **Fallback mechanism**: ability to specify the order of channels for sending messages in case of failure
- **Easy setup and use**

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

## Contributing

We welcome contributions from the community! Please see our [Contributing Guide](CONTRIBUTING.md) for more details on how to get started.

## License

MIT License. See the LICENSE file for details.

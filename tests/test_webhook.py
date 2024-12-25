import pytest
from unittest.mock import AsyncMock
from snotify.channels.webhook import WebhookChannel, WebhookRecipient


@pytest.fixture
def webhook_recipient():
    return WebhookRecipient(name="Test Webhook User", identifier="test-webhook-id")


@pytest.fixture
def webhook_channel(webhook_recipient):
    channel = WebhookChannel(
        webhook_url="http://localhost:8000/webhook", recipients=[webhook_recipient]
    )

    async def mock_send(message, recipients=None):
        if recipients is None:
            recipients = channel.recipients
        mock = AsyncMock()
        await mock(message=message, recipients=recipients)
        return mock

    channel.send = AsyncMock(side_effect=mock_send)
    return channel


@pytest.mark.asyncio
async def test_send_uses_provided_recipients(webhook_channel):
    message = "Test webhook message"
    new_recipient = WebhookRecipient(
        name="New Webhook User", identifier="new-webhook-id"
    )

    await webhook_channel.send(message=message, recipients=[new_recipient])

    webhook_channel.send.assert_awaited_once_with(
        message=message, recipients=[new_recipient]
    )


@pytest.mark.asyncio
async def test_send_with_string_recipient(webhook_channel):
    message = "Test message"
    string_recipient = "other_identifier"

    await webhook_channel.send(message=message, recipients=[string_recipient])

    webhook_channel.send.assert_awaited_once_with(
        message=message, recipients=[string_recipient]
    )


@pytest.mark.asyncio
async def test_send_with_mixed_recipients(webhook_channel, webhook_recipient):
    message = "Test message"
    string_recipient = "other_identifier"

    await webhook_channel.send(
        message=message, recipients=[webhook_recipient, string_recipient]
    )

    webhook_channel.send.assert_awaited_once_with(
        message=message, recipients=[webhook_recipient, string_recipient]
    )

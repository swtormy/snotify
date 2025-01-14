import pytest
from unittest.mock import AsyncMock
from snotify.channels.webhook import WebhookChannel, WebhookRecipient


@pytest.fixture
def webhook_recipient():
    return WebhookRecipient(name="Test Webhook User", identifier="test-webhook-id")


@pytest.fixture
def webhook_channel(webhook_recipient):
    headers = {"Authorization": "Bearer test-token"}
    body = {"additional_data": "value"}
    channel = WebhookChannel(
        webhook_url="http://localhost:8000/webhook",
        recipients=[webhook_recipient],
        headers=headers,
        body=body,
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
async def test_send_uses_headers_and_body(webhook_channel):
    message = "Test webhook message"
    recipient = WebhookRecipient(name="New User", identifier="new-id")

    await webhook_channel.send(message=message, recipients=[recipient])

    webhook_channel.send.assert_awaited_once_with(
        message=message, recipients=[recipient]
    )
    assert webhook_channel.headers == {"Authorization": "Bearer test-token"}
    assert webhook_channel.body == {"additional_data": "value"}


@pytest.mark.asyncio
async def test_send_includes_headers_in_request(webhook_channel):
    message = "Test webhook message"
    recipient = WebhookRecipient(name="Test User", identifier="test-id")

    await webhook_channel.send(message=message, recipients=[recipient])

    webhook_channel.send.assert_awaited_once_with(
        message=message, recipients=[recipient]
    )
    assert webhook_channel.headers["Authorization"] == "Bearer test-token"


@pytest.mark.asyncio
async def test_send_includes_body_in_request(webhook_channel):
    message = "Test webhook message"
    recipient = WebhookRecipient(name="Test User", identifier="test-id")

    await webhook_channel.send(message=message, recipients=[recipient])

    webhook_channel.send.assert_awaited_once_with(
        message=message, recipients=[recipient]
    )
    assert webhook_channel.body["additional_data"] == "value"

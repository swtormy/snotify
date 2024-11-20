import pytest
from unittest.mock import AsyncMock
from snotify.channels.telegram import TelegramChannel, TelegramRecipient


@pytest.fixture
def telegram_recipient():
    return TelegramRecipient(name="Test User", chat_id="123456789")


@pytest.fixture
def telegram_channel(telegram_recipient):
    channel = TelegramChannel(
        bot_token="fake_bot_token", recipients=[telegram_recipient]
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
async def test_send_uses_provided_recipients(telegram_channel):
    message = "Test message"
    new_recipient = TelegramRecipient(name="New User", chat_id="987654321")

    await telegram_channel.send(message=message, recipients=[new_recipient])

    telegram_channel.send.assert_awaited_once_with(
        message=message, recipients=[new_recipient]
    )

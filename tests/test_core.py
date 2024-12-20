import pytest
from unittest.mock import AsyncMock
from snotify.core import Notifier
from snotify.channels.base import BaseChannel, BaseRecipient
from typing import List


class MockChannel(BaseChannel):
    async def send(self, message: str, recipients: List[BaseRecipient] = None):
        pass

    def validate_config(self):
        pass


class MockRecipient(BaseRecipient):
    def get_recipient_id(self) -> str:
        return "mock_id"

    def get_recipient_name(self) -> str:
        return "Mock Recipient"


@pytest.fixture
def notifier():
    return Notifier()


@pytest.fixture
def mock_recipient():
    return MockRecipient()


@pytest.fixture
def mock_channel(mock_recipient):
    channel = MockChannel(recipients=[mock_recipient])
    channel.send = AsyncMock()
    return channel


@pytest.mark.asyncio
async def test_send_success(notifier, mock_channel, mock_recipient):
    notifier.add_channel(mock_channel, "mock")
    notifier.set_fallback_order(["mock"])

    await notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_send_failure_without_fallback(notifier, mock_channel):
    mock_channel.send.side_effect = Exception("Send failed")
    notifier.add_channel(mock_channel, "mock")

    with pytest.raises(Exception, match="Send failed"):
        await notifier.send("Test message")


@pytest.mark.asyncio
async def test_send_failure_with_fallback(notifier, mock_channel, mock_recipient):
    second_channel = MockChannel(recipients=[mock_recipient])
    second_channel.send = AsyncMock()
    mock_channel.send.side_effect = Exception("Send failed")

    notifier.add_channel(mock_channel, "mock")
    notifier.add_channel(second_channel, "second")
    notifier.set_fallback_order(["mock", "second"])

    await notifier.send("Test message")

    mock_channel.send.assert_called_once()
    second_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_fallback_order(notifier, mock_channel, mock_recipient):
    second_channel = MockChannel(recipients=[mock_recipient])
    second_channel.send = AsyncMock()

    mock_channel.send.side_effect = Exception("Send failed")
    notifier.add_channel(mock_channel, "mock")
    notifier.add_channel(second_channel, "second")
    notifier.set_fallback_order(["mock", "second"])

    await notifier.send("Test message")

    mock_channel.send.assert_called_once()
    second_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_add_channel_with_explicit_name(notifier, mock_channel, mock_recipient):
    notifier.add_channel(mock_channel, "custom_name")
    notifier.set_fallback_order(["custom_name"])

    await notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_add_channel_with_auto_name(notifier, mock_channel, mock_recipient):
    notifier.add_channel(mock_channel)
    notifier.set_fallback_order(["mock"])

    await notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_fallback_with_auto_named_channels(notifier, mock_recipient):
    first_channel = MockChannel(recipients=[mock_recipient])
    second_channel = MockChannel(recipients=[mock_recipient])
    first_channel.send = AsyncMock(side_effect=Exception("Send failed"))
    second_channel.send = AsyncMock()

    notifier.add_channel(first_channel)
    notifier.add_channel(second_channel)
    notifier.set_fallback_order(["mock", "mock_1"])

    await notifier.send("Test message")

    first_channel.send.assert_called_once()
    second_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )

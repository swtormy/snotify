import pytest
from unittest.mock import AsyncMock
from snotify.core import Notifier, ANotifier
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
def async_notifier():
    return ANotifier()


@pytest.fixture
def sync_notifier():
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
async def test_async_send_success(async_notifier, mock_channel, mock_recipient):
    async_notifier.add_channel(mock_channel, "mock")
    async_notifier.set_fallback_order(["mock"])

    await async_notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


def test_sync_send_success(sync_notifier, mock_channel, mock_recipient):
    sync_notifier.add_channel(mock_channel, "mock")
    sync_notifier.set_fallback_order(["mock"])

    sync_notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


def test_sync_send_failure_without_fallback(sync_notifier, mock_channel):
    mock_channel.send.side_effect = Exception("Send failed")
    sync_notifier.add_channel(mock_channel, "mock")

    with pytest.raises(Exception, match="Send failed"):
        sync_notifier.send("Test message")


def test_sync_send_failure_with_fallback(sync_notifier, mock_channel, mock_recipient):
    second_channel = MockChannel(recipients=[mock_recipient])
    second_channel.send = AsyncMock()
    mock_channel.send.side_effect = Exception("Send failed")

    sync_notifier.add_channel(mock_channel, "mock")
    sync_notifier.add_channel(second_channel, "second")
    sync_notifier.set_fallback_order(["mock", "second"])

    sync_notifier.send("Test message")

    mock_channel.send.assert_called_once()
    second_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


def test_sync_add_channel_with_explicit_name(
    sync_notifier, mock_channel, mock_recipient
):
    sync_notifier.add_channel(mock_channel, "custom_name")
    sync_notifier.set_fallback_order(["custom_name"])

    sync_notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_add_channel_with_auto_name(async_notifier, mock_channel, mock_recipient):
    async_notifier.add_channel(mock_channel)
    async_notifier.set_fallback_order(["mock"])

    await async_notifier.send("Test message")

    mock_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )


@pytest.mark.asyncio
async def test_fallback_with_auto_named_channels(async_notifier, mock_recipient):
    first_channel = MockChannel(recipients=[mock_recipient])
    second_channel = MockChannel(recipients=[mock_recipient])
    first_channel.send = AsyncMock(side_effect=Exception("Send failed"))
    second_channel.send = AsyncMock()

    async_notifier.add_channel(first_channel)
    async_notifier.add_channel(second_channel)
    async_notifier.set_fallback_order(["mock", "mock_1"])

    await async_notifier.send("Test message")

    first_channel.send.assert_called_once()
    second_channel.send.assert_called_once_with(
        message="Test message", recipients=[mock_recipient]
    )

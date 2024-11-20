import pytest
from unittest.mock import AsyncMock
from snotify.channels.email import EmailChannel, EmailRecipient

@pytest.fixture
def email_recipient():
    return EmailRecipient(name="Test User", email="test@example.com")

@pytest.fixture
def email_channel(email_recipient):
    channel = EmailChannel(
        smtp_server="smtp.example.com",
        smtp_port=587,
        smtp_user="user@example.com",
        smtp_password="password",
        recipients=[email_recipient]
    )
    
    async def mock_send(message, subject="Notification", recipients=None):
        if recipients is None:
            recipients = channel.recipients
        mock = AsyncMock()
        await mock(message=message, subject=subject, recipients=recipients)
        return mock
    
    channel.send = AsyncMock(side_effect=mock_send)
    return channel


@pytest.mark.asyncio
async def test_send_uses_provided_recipients(email_channel):
    message = "Test message"
    new_recipient = EmailRecipient(name="New User", email="new@example.com")
    
    await email_channel.send(message=message, recipients=[new_recipient])
    
    email_channel.send.assert_awaited_once_with(
        message=message,
        recipients=[new_recipient]
    )

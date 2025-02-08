import pytest
from unittest.mock import patch
from queries.tasks import rent_reminder

# Simula o envio de email e verifica se a função foi chamada
@pytest.mark.django_db
@patch("queries.tasks.send_email_reminder")
def test_send_email_reminder(mock_send_mail):
    rent_reminder()
    
    mock_send_mail.assert_called_once()
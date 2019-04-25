import pytest

from simple_app import schema
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db


def test_message_type():
    instance = schema.MessageType()
    assert instance


def test_resolve_all_messages():
    mixer.blend('simple_app.Message')
    mixer.blend('simple_app.Message')
    q = schema.Query()
    response = q.resolve_all_messages(None, None, None)
    assert response.count() == 2
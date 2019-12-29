from base64 import b64encode

import pytest
from pydantic import BaseModel, ValidationError

from aws_lambda_event_models import types


class DummyBase64StrModel(BaseModel):
    data: types.Base64Str


@pytest.fixture()
def fake_data():
    return 'Hello this is a test.'


@pytest.fixture()
def encoded_fake_data(fake_data):
    return b64encode(fake_data.encode('utf8'))


def test_base64_str_properly_decodes_str(fake_data, encoded_fake_data):
    m = DummyBase64StrModel(data=encoded_fake_data.decode("utf8"))

    assert fake_data == m.data


def test_base64_str_properly_decodes_bytes(fake_data, encoded_fake_data):
    m = DummyBase64StrModel(data=encoded_fake_data)

    assert fake_data == m.data


def test_base64_str_raises_validation_error_when_not_bytes_or_str(fake_data, encoded_fake_data):
    with pytest.raises(ValidationError):
        DummyBase64StrModel(data=123)


def test_base64_str_raises_validation_error_when_data_not_properly_base64_encoded(fake_data, encoded_fake_data):
    with pytest.raises(ValidationError) as excinfo:
        DummyBase64StrModel(data='XXXX')

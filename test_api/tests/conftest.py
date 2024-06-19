import pytest
from test_api.src.client.api_client import CurrencyClient


@pytest.fixture
def currency_client():
    return CurrencyClient()

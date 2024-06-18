import pytest
from test_api.src.client.currency_client import CurrencyClient


@pytest.fixture
def currency_client():
    return CurrencyClient()

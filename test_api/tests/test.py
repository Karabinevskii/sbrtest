from datetime import datetime

import pytest

from test_api.src.enums.common import HttpErrorCodes

URL = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='


class TestCurrencyInfo:

    @pytest.mark.parametrize('date', [
        datetime(2023, 7, 13),
        datetime(2023, 8, 19),
        datetime(2023, 12, 29),
    ])
    def test_xml_validity(self, date, currency_client):
        response = currency_client.currency.get_by_id(f"{URL}{date}")
        assert response.status_code == HttpErrorCodes.Ok, f"Неверный статус код: {response.status_code}"

    def test_format(self, ID: str, currency_client):
        response = currency_client.currency.get_by_id(ID)


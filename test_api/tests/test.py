from datetime import datetime
import xml.etree.ElementTree as ET
from logging import root
from xml.dom import minidom
from datetime import datetime as dt
import pytest
import requests

from test_api.src.enums.common import HttpErrorCodes




@pytest.mark.parametrize('date', [
    datetime(2022, 7, 13),
    datetime(2023, 8, 15),
    datetime(2024, 1, 12),
])
class TestCurrencyInfo:

    def test_xml_validity(self, date, currency_client):
        """
        Checking the response status code
        """
        date_reformat = dt.strftime(date, '%d.%m.%Y')
        response = currency_client.currency.get_by_date(date_reformat)
        assert response.status_code == HttpErrorCodes.Ok, f"Wrong status code: {response.status_code}"

    def test_xml_format(self, date, currency_client):
        """
        Checking the XML format
        """
        date_reformat = dt.strftime(date, '%d.%m.%Y')
        response = currency_client.currency.get_by_date(date_reformat)
        assert response.headers["Content-Type"].startswith("application/xml")
        try:
            ET.fromstring(response.content)
        except ET.ParseError as e:
            pytest.fail(f"XML Parsing error: {e}")


        xml_doc = minidom.parseString(response.content)
        root = xml_doc.documentElement

        assert root.tagName == "ValCurs"
        assert root.getAttribute("Date") == date_reformat
        assert root.getAttribute("name") == "Foreign Currency Market"



    def test_currency_values(self, date, currency_client):
        """
        Checking that currency values are numeric and currency codes are valid.
        """
        date_reformat = dt.strftime(date, '%d.%m.%Y')
        response = currency_client.currency.get_by_date(date_reformat)
        xml_doc = minidom.parseString(response.content)
        root = xml_doc.documentElement

        for valute in root.getElementsByTagName('Valute'):
            currency_code = valute.getAttribute('ID')
            assert isinstance(currency_code, str)
            num_code = valute.getElementsByTagName('NumCode')[0].firstChild.nodeValue
            assert isinstance(num_code, int)



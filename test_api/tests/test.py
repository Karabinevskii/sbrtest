import allure
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import datetime as dt
from xml.dom import minidom
import pytest
from test_api.src.enums.common import HttpErrorCodes


@pytest.mark.parametrize('date', [
    datetime(2022, 7, 13),
    datetime(2023, 8, 15),
    datetime(2024, 1, 12),
])
class TestCurrencyInfo:
    """
    Tests to verify information about currency exchange rates.
    """

    def test_xml_validity(self, date, currency_client):
        """
        Checking the response status code
        """
        date_reformat = dt.strftime(date, '%d.%m.%Y')
        response = currency_client.currency.get_by_date(date_reformat)
        assert response.status_code == HttpErrorCodes.Ok, f"Wrong status code: {response.status_code}"

    def test_xml_format(self, date, currency_client):
        """
        Checking the XML response format
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

    @allure.story("Currency values test")
    def test_currency_values(self, date, currency_client):
        """
        Checking the currency values
        - ID - str
        - NumCode - int
        - CharCode - is valid
        - Nominal - int
        - Name - str
        - Value - float
        """
        date_reformat = dt.strftime(date, '%d.%m.%Y')
        response = currency_client.currency.get_by_date(date_reformat)
        xml_doc = minidom.parseString(response.content)
        root = xml_doc.documentElement

        with allure.step(f"Checking the currency values"):
            for valute in root.getElementsByTagName('Valute'):
                valute_id = valute.getAttribute('ID')
                assert isinstance(valute_id, str)

                num_code = valute.getElementsByTagName('NumCode')[0].firstChild.nodeValue
                assert num_code.isdigit(), f"NumCode '{num_code}' is not valid."

                char_code_data = []
                char_code = valute.getElementsByTagName('CharCode')[0].firstChild.nodeValue
                char_code_data.append(char_code)
                assert char_code in char_code_data, f"Char code '{char_code}' is not valid"

                nominal = valute.getElementsByTagName('Nominal')[0].firstChild.nodeValue
                assert nominal.isdigit(), f"Nominal '{nominal}' is not valid"

                currency_names = []
                name = valute.getElementsByTagName('Name')[0].firstChild.nodeValue
                currency_names.append(name)
                assert name in currency_names, f"Name '{name}', is not valid"

                value = valute.getElementsByTagName('Value')[0].firstChild.nodeValue
                value = value.replace(',', '.')
                try:
                    float(value)
                except ValueError:
                    pytest.fail()



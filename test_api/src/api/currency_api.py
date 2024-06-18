from test_api.src.api.base_api import BaseApi


class CurrencyApi(BaseApi):
    PATH = "/scripts/XML_daily.asp?date_req="

    def get_by_id(self, date):
        return self._get(path=f"/{date}")

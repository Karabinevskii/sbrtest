from test_api.src.api.currency_api import CurrencyApi


class CurrencyClient:

    def __init__(self):
        self.currency: CurrencyApi = CurrencyApi()

import requests
from loguru import logger


class BaseApi:
    def __init__(self):
        self.default_headers = {"Content-Type": "application/xml"}
        self.base_url = "http://www.cbr.ru"
        self.entity_path = self.__class__.PATH if hasattr(self.__class__, 'PATH') else ""

    def _get(self, path: str, headers: dict = None, params: dict = None):
        if headers is not None:
            self.default_headers.update(headers)
        url = f"{self.base_url}{self.entity_path}{path}"
        logger.info(f"Headers = {self.default_headers}")
        logger.info(f"{url=}")

        return requests.get(url=url, headers=self.default_headers, params=params)

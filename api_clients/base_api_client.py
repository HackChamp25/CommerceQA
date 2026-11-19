import requests

from config.constants import Headers


class BaseApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update(Headers.JSON)

    def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        return response
    
    def close(self):
        self.session.close()
    

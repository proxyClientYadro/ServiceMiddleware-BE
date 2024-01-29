import requests
from django.conf import settings
from requests import Response
from rest_framework.request import Request

from logger.services.Logger import Logger


class Route:
    """Base Route for communication with third-party services"""

    __ALLOWED_CLIENT_HEADERS = ('Authorization', 'Content-Type',)
    __HEADERS_FOR_DELETE = ('Connection', 'Keep-Alive', 'Content-Length',)

    def __init__(self, request: Request) -> None:
        self.request = request
        Logger().log_client_request(request=self.request)

    def send(self, endpoint: str) -> requests.Response:
        prepared_request = self._prepare_request(endpoint=endpoint)
        response = self._send_request(prepared_request=prepared_request)
        self._filter_response_headers(response=response)
        Logger().log_proxy_request_core_response(response=response)
        return response

    def _prepare_request(self, endpoint: str) -> requests.PreparedRequest:
        url = f'{settings.THIRD_PARTY_APP_URL}/{settings.APP_ID}/{endpoint}/'
        prepared_request = requests.Request(
            method=self.request.method,
            url=url,
            json=self.request.data,
            params=self.request.query_params,
            headers=self.__filter_request_headers(self.request.headers)
        ).prepare()

        return prepared_request

    @staticmethod
    def _send_request(prepared_request: requests.PreparedRequest) -> requests.Response:
        session = requests.Session()
        return session.send(request=prepared_request)

    def __filter_request_headers(self, headers: dict) -> dict:
        return {k: v for k, v in headers.items() if k in self.__ALLOWED_CLIENT_HEADERS}

    def _filter_response_headers(self, response: Response) -> None:
        filtered_headers = {k: v for k, v in response.headers.items() if k not in self.__HEADERS_FOR_DELETE}
        response.headers = filtered_headers

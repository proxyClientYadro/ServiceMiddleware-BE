import requests
from django.conf import settings
from rest_framework.request import Request

from logger.models import LogModel


class Logger:
    
    MODEL_FIELDS = {}

    def log_client_request(self, request: Request) -> None:
        self.MODEL_FIELDS.update({
            'proxy_method': request.method,
            'proxy_url': request.get_full_path(),
            'proxy_request_headers': dict(request.headers),
            'proxy_request_body': request.data,
        })

    def log_proxy_request_core_response(self, response: requests.Response) -> None:
        self.MODEL_FIELDS.update({
            'core_method': response.request.method,
            'core_url': response.request.url,
            'core_request_headers': dict(response.request.headers),
            'core_request_body': response.request.body.decode('utf-8'),
            'core_response_headers': dict(response.headers),
            'core_response_body': response.text,
            'core_response_status_code': response.status_code,
        })

    def log_proxy_response_to_client(self, response: requests.Response) -> None:
        self.MODEL_FIELDS.update({
            'proxy_response_headers': dict(response.headers),
            'proxy_response_body': response.content if response.content else '',
            'proxy_response_status_code': response.status_code,
        })

    def save_to_db(self) -> None:
        if settings.IS_NEED_LOGGER:
            log = LogModel(**self.MODEL_FIELDS)
            log.save()

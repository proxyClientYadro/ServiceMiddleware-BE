from typing import Any

from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request

from rest_framework.response import Response


class HandleStatusCodes:
    def __init__(self, get_response: Any):
        self.get_response = get_response

    def __call__(self, request: Request):
        response = self.get_response(request)

        if 'api/' in request.path:
            return self.handle_api_request(response)
        return response

    def handle_api_request(self, response: Response) -> JsonResponse | Response:
        if response.status_code == 422:
            return self.handle_422_error()
        elif response.status_code == 200:
            return self.handle_200_ok(response)
        else:
            return response

    @staticmethod
    def handle_422_error() -> JsonResponse:
        return JsonResponse(data={'error': 'Unexpected Error'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def handle_200_ok(response: Response) -> JsonResponse:
        if response.data:
            return JsonResponse(data=response.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(data={'status': 'OK'}, status=status.HTTP_200_OK)

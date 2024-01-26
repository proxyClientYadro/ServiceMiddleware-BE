from typing import Any

from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request


class Custom422Error:
    def __init__(self, get_response: Any):
        self.get_response = get_response

    def __call__(self, request: Request):
        response = self.get_response(request)

        if response.status_code == 422 and 'api/' in request.path:
            return JsonResponse({'error': 'Unexpected Error'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return response

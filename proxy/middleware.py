from typing import Any

from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request


class Custom422Error:
    def __init__(self, get_response: Any):
        self.get_response = get_response

    def __call__(self, request: Request):
        response = self.get_response(request)

        if 'api/' in request.path:
            if response.status_code == 422:
                return JsonResponse({'error': 'Unexpected Error'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif response.status_code == 200:
                return JsonResponse({'status': 'OK'}, status=status.HTTP_200_OK)

        return response

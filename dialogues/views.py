from typing import Any
from urllib.request import Request

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.Route import Route
from logger.services.Logger import Logger
from proxy.decorators import handle_json_decode_error


class BaseView(APIView):
    """
    Base class for common CRUD operations.
    Subclasses should define the `get_endpoint` method.
    """

    permission_classes = (IsAuthenticated,)

    @handle_json_decode_error
    def handle_request(self, request: Request, endpoint_suffix: str, *args: Any, **kwargs: dict) -> Response:
        dialogue_id = kwargs.get('dialogue_id')
        endpoint = self.get_endpoint(dialogue_id, endpoint_suffix)
        response = Route(request=request).send(endpoint=endpoint)
        Logger().log_proxy_response_to_client(response=response)
        Logger().save_to_db()
        return response

    @staticmethod
    def get_endpoint(dialogue_id: Any, endpoint_suffix: str) -> str:
        raise NotImplementedError('Subclasses must implement the get_endpoint method')


class DialoguesView(BaseView):
    """View for dialogues CRUD operations"""

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='', *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='', *args, **kwargs)

    def put(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='', *args, **kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='', *args, **kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='', *args, **kwargs)

    def get_endpoint(self, dialogue_id: Any, endpoint_suffix: str) -> str:
        return f'dialogues/{dialogue_id}{endpoint_suffix}' if dialogue_id else f'dialogues{endpoint_suffix}'


class MessagesView(BaseView):
    """View for messages CRUD operations"""

    def get(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='/messages', *args, **kwargs)

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request, endpoint_suffix='/messages', *args, **kwargs)

    def get_endpoint(self, dialogue_id: Any, endpoint_suffix: str) -> str:
        return f'dialogues/{dialogue_id}{endpoint_suffix}' if dialogue_id else f'dialogues{endpoint_suffix}'

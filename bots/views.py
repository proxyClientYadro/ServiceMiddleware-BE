from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bots.services.BotTemplate import BotTemplate
from common.route import Route
from logger.services.Logger import Logger
from proxy.decorators import handle_json_decode_error


class BotView(APIView):
    """Returns the list of existing bots or details for a specific bot"""

    @handle_json_decode_error
    def get(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        bot_id = kwargs.get('bot_id')
        if bot_id is None:
            response = BotTemplate(request=request).send(endpoint='bots')
        else:
            response = Route(request=request).send(endpoint=f'bots/{bot_id}')

        Logger().log_proxy_response_to_client(response=response)
        Logger().save_to_db()

        return response

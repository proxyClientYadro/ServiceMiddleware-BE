from functools import wraps
from typing import Any, Callable

from requests.exceptions import JSONDecodeError
from rest_framework.response import Response


def handle_json_decode_error(request: Callable) -> Any:
    @wraps(wrapped=request)
    def _wrapped_view(*args: Any, **kwargs: dict) -> Response:
        response = request(*args, **kwargs)
        try:
            if response.content:
                data = response.json()
                return Response(data=data, status=response.status_code, headers=response.headers)
            else:
                return Response(status=response.status_code, headers=response.headers)
        except JSONDecodeError:
            return Response(data=response.text, status=response.status_code, headers=response.headers)

    return _wrapped_view

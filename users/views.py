from typing import Any

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.route import Route
from logger.services.Logger import Logger
from proxy.decorators import handle_json_decode_error
from users.models import UserModel
from users.serializer import UserSerializer, LoginSerializer

from django.contrib.auth import authenticate, login


class BaseUserOperationView(APIView):
    """Base class for user registration and login"""

    route_class: Any = Route
    endpoint: str = None
    permission_classes = (IsAuthenticated,)

    @handle_json_decode_error
    def handle_request(self, request: Request) -> Response:
        response = self.route_request(request)
        self._log_and_save(response=response)
        return response

    def route_request(self, request: Request) -> Response:
        return self.route_class(request=request).send(endpoint=self.endpoint)

    @staticmethod
    def _log_and_save(response: Response) -> None:
        Logger().log_proxy_response_to_client(response=response)
        Logger().save_to_db()


class UserRegistrationView(BaseUserOperationView, CreateAPIView):
    """Registers a user in the app and the 3rd-party service"""

    endpoint = 'users'
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        response = self.handle_request(request=request)
        return self._create_user_or_unprocessable_entity(response=response, request=request, *args, **kwargs)

    def _create_user_or_unprocessable_entity(self,
                                             response: Response,
                                             request: Request,
                                             *args: Any,
                                             **kwargs: dict) -> Response:
        if response.status_code == 200:
            return self.create(request=request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(BaseUserOperationView):
    """Login user and gets an access token from the 3rd-party service"""

    endpoint = 'users/login'
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = self.handle_request(request=request)
            return self._login_or_unprocessable_entity(response, request)

    @staticmethod
    def _login_or_unprocessable_entity(response: Response, request: Request) -> Response:
        if response.status_code == 200:
            user = authenticate(request, email=response.data.get('email'), password=response.data.get('password'))
            login(request=request, user=user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LogoutView(BaseUserOperationView):
    """Logs out a user from the third-party service"""

    endpoint = 'users/logout'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationView(BaseUserOperationView):
    """Base class for email verification views"""

    endpoint: str = 'email-verification/verify'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationCheckView(EmailVerificationView):
    """Checks email verification status"""

    endpoint = 'users/email-verification/check'


class EmailVerificationResendView(EmailVerificationView):
    """Resends email verification"""

    endpoint = 'users/email-verification/resend'


class EmailVerificationVerifyView(EmailVerificationView):
    """Verifies email"""

    endpoint = 'users/email-verification/verify'

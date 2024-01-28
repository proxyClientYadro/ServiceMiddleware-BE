from typing import Any

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.route import Route
from logger.services.Logger import Logger
from proxy.decorators import handle_json_decode_error
from users.models import UserModel
from users.serializer import LoginSerializer, UserSerializer


class BaseUserOperationView(APIView):
    """Base class for user registration and login"""

    route_class: Any = Route
    endpoint: str = None

    @handle_json_decode_error
    def handle_request(self, request: Request) -> Response:
        if request.user.is_authenticated:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {request.user.access_token}'

        response = self._route_request(request)
        self._log_and_save(response=response)
        return response

    def _route_request(self, request: Request) -> Response:
        return self.route_class(request=request).send(endpoint=self.endpoint)

    @staticmethod
    def _log_and_save(response: Response) -> None:
        Logger().log_proxy_response_to_client(response=response)
        Logger().save_to_db()


class UserRegistrationView(BaseUserOperationView, CreateAPIView):
    """Registers user in the app and the 3rd-party service"""

    endpoint = 'users'
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        response = self.handle_request(request=request)
        return self._create_user_or_return_error(response=response, request=request, *args, **kwargs)

    def _create_user_or_return_error(self,
                                     response: Response,
                                     request: Request,
                                     *args: Any,
                                     **kwargs: dict) -> Response:
        response_status_code = response.status_code
        if response_status_code == 200:
            return self.create(request=request, *args, **kwargs)
        elif response_status_code == 409:
            return Response(data={'error': 'Пользователь уже зарегистрирован'}, status=status.HTTP_409_CONFLICT)
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
            return self._login_or_unprocessable_entity(response=response, request=request)

    @staticmethod
    def _login_or_unprocessable_entity(response: Response, request: Request) -> Response:
        if response.status_code == 200:
            user: UserModel = authenticate(request, email=request.data.get('email'),
                                           password=request.data.get('password'))
            login(request=request, user=user)
            user.set_access_token(access_token=response.data['result'].get('access_token'))
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LogoutView(BaseUserOperationView):
    """Logs out a user from the third-party service"""

    endpoint = 'users/logout'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        response = self.handle_request(request=request)
        return self._logout_or_unprocessable_entity(response=response, request=request)

    @staticmethod
    def _logout_or_unprocessable_entity(response: Response, request: Request) -> Response:
        if response.status_code == 204:
            user = UserModel.objects.get(uuid=request.user.uuid)
            user.set_access_token(access_token=None)
            logout(request=request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class EmailVerificationView(BaseUserOperationView):
    """Base class for email verification views"""

    endpoint: str = 'email-verification/verify'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationCheckView(BaseUserOperationView):
    """Checks email verification status"""

    endpoint = 'users/email-verification/check'

    def get(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationResendView(EmailVerificationView):
    """Resends email verification"""

    endpoint = 'users/email-verification/resend'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationVerifyView(EmailVerificationView):
    """Verifies email"""

    endpoint = 'users/email-verification/verify'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)

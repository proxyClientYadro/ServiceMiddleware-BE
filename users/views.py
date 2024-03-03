from typing import Any

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.Route import Route
from logger.services.Logger import Logger
from proxy.decorators import handle_json_decode_error
from users.models import UserModel
from users.serializer import LoginSerializer, UserSerializer


class BaseUserOperationView(APIView):
    """Base class for users operations"""

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
        return self._create_user_or_handled_error(response=response, request=request, *args, **kwargs)

    @staticmethod
    def _create_user_or_handled_error(
            response: Response,
            request: Request,
            *args: Any,
            **kwargs: dict
    ) -> Response:
        response_status_code = response.status_code
        if response_status_code == 200:
            return response
        else:
            return Response(data=response.data, status=response.status_code)


class LoginView(BaseUserOperationView):
    """Login user and get an access token from the 3rd-party service"""

    endpoint = 'users/login'
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        response = self.handle_request(request=request)
        return self._login_or_handled_error(response=response, request=request)

    def _login_or_handled_error(self, response: Response, request: Request) -> Response:

        if response.status_code == 200:
            user: UserModel = authenticate(request, email=request.data.get('email'),
                                           password=request.data.get('password'))
            login(request=request, user=user)
            print(response.data['result'].get('access_token'))
            user.set_access_token(access_token=response.data['result'].get('access_token'))

            serializer = self.serializer_class(user)
            print(serializer.data)
            response.data = {'result': serializer.data}

            return Response(data=response.data, status=response.status_code)
        else:
            return Response(data=response.data, status=response.status_code)


class LogoutView(BaseUserOperationView):
    """Logout user from the app and delete acces_token from the third-party service"""

    endpoint = 'users/logout'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        response = self.handle_request(request=request)
        return self._logout_or_handled_error(response=response, request=request)

    @staticmethod
    def _logout_or_handled_error(response: Response, request: Request) -> Response:
        if response.status_code == 204:
            user = UserModel.objects.get(uuid=request.user.uuid)
            user.set_access_token(access_token=None)
            logout(request=request)
            return Response(data=response.data, status=response.status_code)
        else:
            return Response(data=response.data, status=response.status_code)


class EmailVerificationView(BaseUserOperationView):
    """Email verification view"""

    endpoint: str = 'email-verification/verify'
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationCheckView(BaseUserOperationView):
    """Check email verification status"""

    endpoint = 'users/email-verification/check'

    def get(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationResendView(EmailVerificationView):
    """Resend email verification"""

    endpoint = 'users/email-verification/resend'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)


class EmailVerificationVerifyView(EmailVerificationView):
    """Verify the email"""

    endpoint = 'users/email-verification/verify'

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.handle_request(request=request)

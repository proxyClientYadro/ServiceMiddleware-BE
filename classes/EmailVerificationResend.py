from .CustomRoute import CustomRoute
from rest_framework.views import APIView


class EmailVerificationResend(CustomRoute, APIView):

    def get_method(self):
        return "POST"

    def get_patch(self):
        return f"/users/email-verification/resend"

from django.urls import path

from users.views import (EmailVerificationCheckView,
                         EmailVerificationResendView,
                         EmailVerificationVerifyView, LoginView, LogoutView,
                         UserRegistrationView)

urlpatterns = [
    path('', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-verification/check/', EmailVerificationCheckView.as_view(), name='email_check'),
    path('email-verification/resend/', EmailVerificationResendView.as_view(), name='email_resend'),
    path('email-verification/verify/', EmailVerificationVerifyView.as_view(), name='email_login')
]

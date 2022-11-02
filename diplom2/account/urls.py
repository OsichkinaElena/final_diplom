from django.urls import path, re_path, include
from .views import LoginAccount, ContactView, AccountDetails, ConfirmAccount, RegisterAccount
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

urlpatterns = [

    path('register', RegisterAccount.as_view(), name='user-register'),
    path('register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('details', AccountDetails.as_view(), name='user-details'),
    path('contact', ContactView.as_view(), name='user-contact'),
    path('login', LoginAccount.as_view(), name='user-login'),
    path('password_reset', reset_password_request_token, name='password-reset'),

]
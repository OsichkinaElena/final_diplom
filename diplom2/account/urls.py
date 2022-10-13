from django.urls import path, re_path, include



urlpatterns = [
    # path('users/', RegistrationAPIView.as_view()),
    # path('users/login/', LoginAPIView.as_view()),
    # path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('user/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
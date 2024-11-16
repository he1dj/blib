from django.urls import path, include
from .views import LoginView, SignupView, PasswordSetView, PasswordChangeView, PasswordResetView


urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('password_set/', PasswordSetView.as_view(), name='account_set_password'),
    path('password_change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password_reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path("account/", include("allauth.urls")),
]

from allauth.account.views import (
    LoginView as Login, 
    SignupView as Signup, 
    PasswordChangeView as PasswordChange, 
    PasswordSetView as PasswordSet, 
    PasswordResetView as PasswordReset, 
)


class LoginView(Login):
    template_name = 'users/login.html'
    

class SignupView(Signup):
    template_name = 'users/signup.html'
    

class PasswordChangeView(PasswordChange):
    template_name = 'users/password_change.html'
    

class PasswordSetView(PasswordSet):
    template_name = 'users/password_set.html'
    success_url = 'user_profiles:profile'
    

class PasswordResetView(PasswordReset):
    template_name = 'users/password_reset.html'
    
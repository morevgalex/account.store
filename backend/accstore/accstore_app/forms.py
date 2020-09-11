from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32)


class RegisterForm(LoginForm):
    email = forms.EmailField()
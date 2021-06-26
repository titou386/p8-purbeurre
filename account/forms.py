from django import forms
from django.forms import ModelForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class CleanPasswordMixin:
    def clean_password2(self):
        if not self.cleaned_data.get('password1') and self.instance.user:
            return None

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Le mot de passe ne correspond pas")
        return password2


class CleanEmailMixin:
    def clean_email(self):
        if hasattr(self, 'user'):
            if self.cleaned_data['email'] and \
               self.cleaned_data['email'].lower() == self.user.email:
                return None

        email = self.cleaned_data['email'].lower()
        dir(self)
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("L'email est déjà enregistré")
        return email


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms
                                .EmailInput(attrs={'autofocus': True,
                                                   'class': 'form-control'}))
    password = forms.CharField(label='Mot de passe', widget=forms
                               .PasswordInput(attrs={'autocomplete':
                                                     'current-password',
                                                     'class': 'form-control'}))


class RegisterForm(ModelForm, CleanPasswordMixin):
    username = forms.CharField(label='Pseudo', min_length=4, max_length=150,
                               widget=forms.TextInput(attrs={'autofocus': True,
                                                             'class':
                                                             'form-control'}))
    email = forms.EmailField(label='Email', widget=forms
                             .EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Mot de passe', widget=forms
                                .PasswordInput(attrs={'class':
                                                      'form-control'}))

    password2 = forms.CharField(label='Vérification du mot de passe',
                                widget=forms
                                .PasswordInput(attrs={'class':
                                                      'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        return self.cleaned_data['username']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("L'email est déjà enregistré")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class ProfileUpdateForm(ModelForm, CleanPasswordMixin):
    email = forms.EmailField(required=False,
                             label='Email',
                             widget=forms
                             .EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=False,
                                label='Mot de passe', widget=forms
                                .PasswordInput(attrs={'class':
                                                      'form-control'}))

    password2 = forms.CharField(required=False,
                                label='Vérification du mot de passe',
                                widget=forms
                                .PasswordInput(attrs={'class':
                                                      'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

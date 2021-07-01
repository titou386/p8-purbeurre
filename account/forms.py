from django import forms
from django.forms import ModelForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm


class CleanPasswordMixin(ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms
                                .PasswordInput(attrs={'class':
                                                      'form-control'}))

    password2 = forms.CharField(label='Vérification du mot de passe',
                                widget=forms
                                .PasswordInput(attrs={'class':
                                                      'form-control'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Le mot de passe ne correspond pas")
        return password2


class CleanEmailMixin(ModelForm):
    email = forms.EmailField(label='Email', widget=forms
                             .EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
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


class RegisterForm(CleanEmailMixin, CleanPasswordMixin):
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

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class PasswordUpdateForm(CleanPasswordMixin):
    class Meta:
        model = User
        fields = ['password1', 'password2']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            self.user.save()
        return self.user


class EmailUpdateForm(CleanEmailMixin):
    class Meta:
        model = User
        fields = ['email']

    def save(self, user, commit=True):
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

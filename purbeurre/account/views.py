from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DeleteView, CreateView
from django.views.generic.edit import ProcessFormView
from django.contrib.auth.views import LoginView

from .models import Substitution, User
from django.contrib import messages

from .forms import RegisterForm, LoginForm

class IndexView(LoginView):
    template_name = "account/index.html"
    form_class = LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = '/account/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/account/')
        return super().dispatch(request, *args, **kwargs)

class SubstitutionView(LoginRequiredMixin, ListView):
    model = Substitution
    template_name = 'account/substitution.html'
    context_object_name = 'substitutions'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Substitution
    success_url = '/account/substitution/'

class SaveView(LoginRequiredMixin, CreateView):
    model = Substitution
    success_url = '/account/substitution/'

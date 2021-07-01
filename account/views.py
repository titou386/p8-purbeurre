from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from django.views.generic import (
    ListView, DeleteView, CreateView, FormView, View)

from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect

from .models import Substitution
from search.models import Product

from .forms import RegisterForm, LoginForm, PasswordUpdateForm, EmailUpdateForm


class Session(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class IndexView(LoginView):
    template_name = "account/index.html"
    form_class = LoginForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = '/account/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account')
        return super().dispatch(request, *args, **kwargs)


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordUpdateForm
    template_name = 'account/profile_update.html'
    success_url = '/account/'


class EmailUpdateView(LoginRequiredMixin, FormView):
    form_class = EmailUpdateForm
    template_name = 'account/profile_update.html'
    success_url = '/account/'

    def form_valid(self, form):
        form.save(self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class MySubstitutionsView(Session, ListView):
    model = Substitution
    template_name = 'account/my_substitutions.html'
    context_object_name = 'substitutions'


class DeleteView(Session, DeleteView):
    model = Substitution
    success_url = '/account/substitutions/'


class SaveView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        Substitution(user=request.user, substitution=Product.objects
                     .get(id=kwargs['product'])).save()
        return redirect('my_substitutions')

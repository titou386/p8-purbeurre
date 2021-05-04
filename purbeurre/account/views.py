from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DeleteView, CreateView, View
from django.views.generic.edit import ProcessFormView
from django.contrib.auth.views import LoginView

from .models import Substitution, User
from search.models import Product
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

class MySubstitutionsView(LoginRequiredMixin, ListView):
    model = Substitution
    template_name = 'account/my_substitutions.html'
    context_object_name = 'substitutions'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Substitution
    success_url = '/account/substitutions/'

class SaveView(LoginRequiredMixin, View):
    http_method_names = ['post']
#    model = Substitution
#    success_url = '/account/substitution/'
#    fields = ['user', 'substitution']
#
#    def get_queryset(self):
#        print(dir(self.request))
#        return super().get_queryset()
    def post(self, request, *args, **kwargs):
        Substitution(user=request.user, substitution=Product.objects.get(id=kwargs['product'])).save()
        return redirect('my_substitutions')

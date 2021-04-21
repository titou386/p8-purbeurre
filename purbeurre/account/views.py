#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import FormView, ListView, View
from django.contrib.auth.views import LoginView
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm

from .models import User, Substitution
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm


class IndexView(LoginView):
    template_name = "account/index.html"
#    success_url = "/account/"
#    form_class = AuthForm



class RegisterView(FormView):
#    model = User
#    fields = ['username', 'email', 'password']
#    success_url = '/account/'
    form_class = RegisterForm
    template_name = 'account/register.html'

    def post(self, request):
        f = RegisterForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('/account/')
        else:
            f = RegisterForm()
        return render(request, 'account/register.html', {'form': f})

#@method_decorator(login_required, name='get_queryset')
class SubstitutionView(LoginRequiredMixin, ListView):
#    login_url = '/account/'
    model = Substitution
    template_name = 'account/substitution.html'
#    redirect_field_name = 'redirect_to'

#    model = Substitution
#    queryset = Substitution.objects.filter(id=?)
#    template_name = 'account/substitution.html'
    context_object_name = 'substitutions'

    def get_queryset(self):
#        if self.request.user is None
#            return redirect('/account/')
        return Substitution.objects.filter(user_id=self.request.user.id)


from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'), # next_page="/account/"
    path('register/', views.RegisterView.as_view(), name='register'),
    path('substitution/', views.SubstitutionView.as_view(), name='substitution'),
    path('substitution/<pk>/delete/', views.DeleteView.as_view()),
    path('substitution/<int:index>/save/', views.SaveView.as_view())
]

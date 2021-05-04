from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'), # next_page="/account/"
    path('register/', views.RegisterView.as_view(), name='register'),
    path('substitutions/', views.MySubstitutionsView.as_view(), name='my_substitutions'),
    path('substitutions/<pk>/delete/', views.DeleteView.as_view()),
    path('substitutions/<int:product>/save/', views.SaveView.as_view())
]

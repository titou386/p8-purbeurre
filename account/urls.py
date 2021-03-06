from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('pass_update/', views.PasswordUpdateView.as_view(),
         name='pass_update'),

    path('email_update/', views.EmailUpdateView.as_view(),
         name='email_update'),

    path('substitutions/', views.MySubstitutionsView.as_view(),
         name='my_substitutions'),

    path('substitutions/<pk>/delete/', views.DeleteView.as_view(),
         name='delete'),
    path('substitutions/<int:product>/save/', views.SaveView.as_view(),
         name='save')
]

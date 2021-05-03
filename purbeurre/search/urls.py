from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('substitution/', views.SubstitutionView.as_view(), name='search')
]

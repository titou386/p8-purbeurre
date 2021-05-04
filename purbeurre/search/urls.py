from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<pk>/substitutions/', views.SubstitutionsView.as_view(), name='substitutions'),
    path('product/<pk>/', views.ProductDetailsView.as_view(), name='details'),
    path('search/', views.ResultsView.as_view(), name='search')
]

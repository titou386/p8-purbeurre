from django.shortcuts import render
from .models import Product, Category
from django.views.generic import ListView, DetailView
from django.db.models import Count

def index(request):
    return render(request, 'search/index.html')

class ResultsView(ListView):
    model = Product
    template_name = 'search/results.html'
    context_object_name = 'results'

    def get_queryset(self):
        return super().get_queryset().filter(name__icontains=self.request.GET['query'])

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET['query']
        return context

class SubstitutionsView(ListView):
    model = Product
    template_name = 'search/substitutions.html'
    context_object_name = 'substitutions'

    def get_queryset(self):
        p = Product.objects.get(id=self.kwargs['pk'])

        return super().get_queryset()\
            .filter(categories__in=p.categories.all())\
            .filter(nutriscore__lte=p.nutriscore)\
            .exclude(id=p.id)\
            .values('id', 'name', 'image_url', 'nutriscore')\
            .annotate(q_count=Count('id'))\
            .order_by('-q_count')[:30]



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orig_product'] = Product.objects.get(id=self.kwargs['pk'])
        return context



class ProductDetailsView(DetailView):
    model = Product
    template_name = 'search/details.html'
    context_object_name = 'details'

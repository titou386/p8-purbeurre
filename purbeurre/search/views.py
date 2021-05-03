from django.shortcuts import render
from .models import Product
from django.views.generic import ListView

def index(request):
    return render(request, 'search/index.html')

class SubstitutionView(ListView):
    model = Product
    template_name = 'search/results.html'
    context_object_name = 'substitutions'

    def get_queryset(self):
        return super().get_queryset().filter(name__icontains=self.request.GET['query'])

#    def get(self, request, *args, **kwargs):
#        print(self.page_kwarg)
#        return super().get(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        print(dir(request.content_params))
        return super().get(request, *args, **kwargs)

class SubstitutionsView(ListView):
    model = Category
    template_name = 'search/substitutions.html'
    context_object_name = 'substitutions'
    #def product_search(query):
    #    product = Product.objects.filter(name__iexact=query).first()
    #    return product if product else Product.objects.filter(name__icontains=query).first()

    def get_queryset(self):
        # query set de categories du produit rechecrché
#        categories = Category.objects.filter(products=product)
#    
#        # query set de tous les produits uniques sup ou égale au nutriscore des catégories du produit recherché
#        products_in_categories = categories.filter(products__nutriscore__lte=product.nutriscore).values('products').distinct()
#        
#        # query set du Classement du plus grand nombre de categories au plus petit en excluant le produit lui même.
##        p = Product.objects.filter(id__in=products_in_categories).annotate(q_count=Count('category__products')).order_by("-q_count").exclude(id=product.id)
#    
#        # ou ( mais resultats différents )
#        products_in_categories.annotate(q_count=Count('products')).order_by("-q_count").exclude(id=product.id)
        p = Product.objects.get(id=self.kwargs['pk'])
        return super().get_queryset().filter(products=p).filter(products__nutriscore__lte=p.nutriscore).values('products').distinct().annotate(q_count=Count('products')).order_by("-q_count").exclude(id=p.id)[:30]
#        print(self.kwargs)
#        return super().get_queryset()


class ProductDetailsView(DetailView):
    model = Product
    template_name = 'search/details.html'
    context_object_name = 'details'

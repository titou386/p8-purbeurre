from django.forms import ModelForm
from search.models import Product, Category, ProductCategory

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'image_url', 'nutriscore']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['product', 'category']

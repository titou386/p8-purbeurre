from django.test import TestCase
from django.urls import reverse

from search.models import Product, Category


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class ResultsViewTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Pâte à tartiner aux noisettes",
                               code="758511125439",
                               image_url="https://nutella.com/product.jpg",
                               nutriscore='e')
        Product.objects.create(name="Chocolat aux noisettes",
                               code="758516525439",
                               image_url="https://milka.com/product.jpg",
                               nutriscore='d')

    def test_result_returns_1_product(self):
        response = self.client.get(reverse('search'), {'query': 'tartiner'})
        self.assertEqual(len(response.context_data['results']), 1)

    def test_result_returns_2_products(self):
        response = self.client.get(reverse('search'), {'query': 'noisettes'})
        self.assertEqual(len(response.context_data['results']), 2)

    def test_result_returns_0_product(self):
        response = self.client.get(reverse('search'), {'query': 'confiture'})
        self.assertEqual(len(response.context_data['results']), 0)


class SubstitutionViewTestCase(TestCase):
    def setUp(self):
        p1 = Product.objects.create(name="Nutella 650g",
                                    code="758511125439",
                                    image_url="https://nutella.fr/product.jpg",
                                    nutriscore='e')
        p2 = Product.objects.create(name="Pâte à tartiner aux noisettes",
                                    code="5469725548545",
                                    image_url="https://choco.com/product.jpg",
                                    nutriscore='d')
        c = Category.objects.create(name='Pâte à tartiner')
        c.products.add(p1)
        c.products.add(p2)

    def test_substitution_returns_1_product(self):
        p = Product.objects.get(code="758511125439")
        response = self.client.get(f'/product/{p.id}/substitutions/')
        self.assertEqual(len(response.context_data['substitutions']), 1)

    def test_substitutions_returns_0_product(self):
        p = Product.objects.get(code="5469725548545")
        response = self.client.get(f'/product/{p.id}/substitutions/')
        self.assertEqual(len(response.context_data['substitutions']), 0)

class LegalPageTestCase(TestCase):
    def test_legal_page(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)

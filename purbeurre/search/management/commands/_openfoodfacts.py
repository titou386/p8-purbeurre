"""openfoodfacts.py."""
from search.models import Product, Category
from django.db import IntegrityError, DataError
import requests
import json
import logging


class OpenFoodFacts:
    """Retrieves data from the Open Food Facts API."""

    def __init__(self, nb_of_categories, nb_of_products):
        """Open Food Facts' contructor require 2 arguments."""
        self.nb_of_categories = nb_of_categories
        self.nb_of_products = nb_of_products
        self.categories = []
        self.get_categories()

    def get_categories(self):
        """Method get_categories.

        Retrieve from the API and fill 'self.categories' variable with
        a decreasing ordered list.
        Returns:
            Nothing (fill up self.categories list)
        """
        self.categories = [None for e in range(self.nb_of_categories)]

        r = requester('https://fr.openfoodfacts.org/categories.json')

        for category in r['tags']:
            for i in range(len(self.categories)):
                if self.categories[i] is None or \
                   self.categories[i]["products"] < category["products"]:

                    self.categories.insert(i, category)
                    self.categories.pop(len(self.categories) - 1)
                    break

    def get_products(self, category):
        """Method get_products.

        Retrieve x(see constants.py for the number) products of the category
        contained in the first element of 'self.categories' list.
        Returns:
            Dict value if it succeeded
            None if it failed
        """
        try:
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': category['id'],
                'tagtype_1': 'countries',
                'tag_contains_1': 'contains',
                'tag_1': 'France',
                'page_size': self.nb_of_products,
                'json': 'true'
            }

            r = requester('https://world.openfoodfacts.org/cgi/search.pl',
                          params=payload)

            return r['products']
        except(IndexError, TypeError) as e:
            logging.error('openfoodfacts.py:OpenFoodFacts:get_products:{}'.format(e))
            return None

    def insert_product(self, product_dict):
        """Insert one product in database.

        Parameters:
            product_dict(dict): Contains all tags from
                openfoodfacts api. Some tags are selected for the
                product insertion.

        Returns:
            Nothing.
        """
        product_tags = {}
        # association = {'column DB': 'OpenFoodFacts_tag'}
        association = {'code': 'code',
                       'name': ['product_name', 'product_name_fr', 'generic_name', 'generic_name_fr'],
                       'image_url': 'image_url',

                       'quantity': 'quantity',
                       'nutriscore': 'nutriscore_grade',

                       'energy_kcal_100g': 'nutriments:energy-kcal_100g',
                       'fat_100g': 'nutriments:fat_100g',
                       'saturated_fat_100g': 'nutriments:saturated-fat_100g',
                       'carbohydrates_100g': 'nutriments:carbohydrates_100g',
                       'sugars_100g': 'nutriments:sugars_100g',
                       'fiber_100g': 'nutriments:fiber_100g',
                       'proteins_100g': 'nutriments:proteins_100g',
                       'salt_100g': 'nutriments:salt_100g',

                       'energy_kcal_100g_unit': 'nutriments:energy-kcal_unit',
                       'fat_100g_unit': 'nutriments:fat_unit',
                       'saturated_fat_100g_unit': 'nutriments:saturated-fat_unit',
                       'carbohydrates_100g_unit': 'nutriments:carbohydrates_unit',
                       'sugars_100g_unit': 'nutriments:sugars_unit',
                       'fiber_100g_unit': 'nutriments:fiber_unit',
                       'proteins_100g_unit': 'nutriments:proteins_unit',
                       'salt_100g_unit': 'nutriments:salt_unit'
                       }
        for key in association:
            try:
                if isinstance(association[key], list):
                    for tag in association[key]:
                        if tag in product_dict and product_dict[tag] != '':
                            product_tags[key] = product_dict[tag]
                            break
                elif has_colun(association[key]):
                    key1, key2 = association[key].split(':')
                    product_tags[key] = product_dict[key1][key2]
                else:
                    product_tags[key] = product_dict[association[key]]
                if isinstance(product_tags[key], str):
                    product_tags[key] = product_tags[key].replace('\n', ' ')
            except KeyError:
                pass

        try:
            prod_obj = Product.objects.get_or_create(**product_tags)[0]
        except(IntegrityError, DataError) as e:
            logging.error('openfoodfacts.py:OpenFoodFacts:insert_product:{}'.format(e))
            return

        # Categories insertion.
        for key in ("categories", "categories_old"):
            try:
                # Some values in key are wrongly formatted
                product_dict[key] = product_dict[key].replace('\n', ' ')
                for pattern in (', ', ',', '  ', ' - '):
                    val_list = product_dict[key].split(pattern)
                    if len(val_list) > 1:
                        break

                # Re-check every items list
                copy = val_list.copy()
                for val in copy:
                    for pattern in (', ', ',', '  ', ' - '):
                        tmp = val.split(pattern)
                        if len(tmp) > 1:
                            val_list.remove(val)
                            for t in tmp:
                                val_list.append(t)
                            break

                for value in val_list:
                    if has_colun(value):
                        value = value[3:]
                    cat_obj = self.insert_category(value)
                    if cat_obj:
                        self.insert_product_category(prod_obj, cat_obj)
            except KeyError:
                pass

    def insert_product_category(self, product_object, category_object):
        """Insert one association (product, category) in database.

        Parameters:
            product_id(int/str): Product index
            category_id(int/str): Category index

        Returns:
            Nothing
        """
        try:
            category_object.products.add(product_object)
        except(IntegrityError) as e:
            logging.error('openfoodfacts.py:OpenFoodFacts:insert_product_category:{}'.format(e))

    def insert_category(self, category_name):
        """Insert one category in database.

        Parameters:
            category_name(str): Category should be inserted

        Returns:
            int: Return an index
        """
        try:
            return Category.objects.get_or_create(name=category_name)[0]
        except(IntegrityError, DataError) as e:
            logging.error('openfoodfacts.py:OpenFoodFacts:insert_category:{}'.format(e))
            return


def has_colun(text):
    """Test if a ':' is in this string.

    Return true or false
    """
    return False if text.find(':') == -1 else True


def requester(url, **product_dict):
    """Similar to requests.get.

    Parameters:
        url(str): url with http://

        parameter named:
            params(key)(str) take same paramaters than requests

    Returns:
        dict: json converted
        None if it failed
    """
    try:
        if ('params' in product_dict):
            r = requests.get(url, product_dict['params'])
        else:
            r = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if r.ok:
        return json.loads(r.text)
    else:
        logging.error('openfoodfacts.py:requester:Une erreur s\'est produite \
lors de la récupération des données')
        logging.error('openfoodfacts.py:requester:Code erreur HTTP : {}'.
                      format(r.status_code))
    return None

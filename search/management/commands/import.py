from django.core.management.base import BaseCommand
from search.management.commands._openfoodfacts import OpenFoodFacts


class Command(BaseCommand):
    help = 'Import data into database from OpenFoodFacts'
    missing_args_message = 'Required arguments missing, see the documentation.'
    requires_migrations_checks = True
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('-c', '--categories', type=int, nargs='?',
                            required=True, help='Number of categories impoted')
        parser.add_argument('-p', '--products', type=int, nargs='?',
                            required=True,
                            help='\
Number of products imported in each category')

    def handle(self, *args, **options):
        i = 0
        openfoodfact = OpenFoodFacts(options['categories'],
                                     options['products'])
        for cat in openfoodfact.categories:
            prods_dict_lst = openfoodfact.get_products(cat)
            if prods_dict_lst:
                for product_dict in prods_dict_lst:
                    openfoodfact.insert_product(product_dict)
            i += 1
            self.stdout.write("{}% éffectué ..."
                              .format(int(i / options['categories'] * 100)))
        self.stdout.write(self.style.SUCCESS('OK'))

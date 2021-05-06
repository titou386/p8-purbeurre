from django.db import models


class Product(models.Model):
    code = models.BigIntegerField(unique=True, default=None)
    name = models.CharField(max_length=100, default=None)
    image_url = models.CharField(max_length=150, default=None)

    quantity = models.CharField(max_length=100, null=True, blank=True)
    nutriscore = models.CharField(max_length=1, default=None)

    energy_kcal_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fat_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saturated_fat_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    carbohydrates_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sugars_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fiber_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    proteins_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salt_100g = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    energy_kcal_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    fat_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    saturated_fat_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    carbohydrates_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    sugars_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    fiber_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    proteins_100g_unit = models.CharField(max_length=10, null=True, blank=True)
    salt_100g_unit = models.CharField(max_length=10, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    products = models.ManyToManyField(Product, related_name="categories")

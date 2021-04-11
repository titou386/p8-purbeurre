from django.db import models


class Product(models.Model):
    code = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=150)

    quantity = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)

    energy_kcal_100g = models.DecimalField(max_digits=6, decimal_places=2)
    fat_100g = models.DecimalField(max_digits=5, decimal_places=2)
    saturated_fat_100g = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates_100g = models.DecimalField(max_digits=5, decimal_places=2)
    sugars_100g = models.DecimalField(max_digits=5, decimal_places=2)
    fiber_100g = models.DecimalField(max_digits=5, decimal_places=2)
    proteins_100g = models.DecimalField(max_digits=5, decimal_places=2)
    salt_100g = models.DecimalField(max_digits=5, decimal_places=2)

    energy_kcal_100g_unit = models.CharField(max_length=10)
    fat_100g_unit = models.CharField(max_length=10)
    saturated_fat_100g_unit = models.CharField(max_length=10)
    carbohydrates_100g_unit = models.CharField(max_length=10)
    sugars_100g_unit = models.CharField(max_length=10)
    fiber_100g_unit = models.CharField(max_length=10)
    proteins_100g_unit = models.CharField(max_length=10)
    salt_100g_unit = models.CharField(max_length=10)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'category'], name="product-categorised")
        ]

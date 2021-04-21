from django.db import models
from django.contrib.auth.models import AbstractUser #, User
from search.models import Product


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(('Email'), unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = []


class Substitution(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    substitution_id = models.ForeignKey(Product, related_name='substitution', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'product_id', 'substitution_id')

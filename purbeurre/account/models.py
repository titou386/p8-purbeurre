from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_unicode_slug
from search.models import Product


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(('Email'), unique=True)
    username = models.CharField(help_text='\
Champ requis. 150 characters maximum. Lettres, \
chiffres et @/./+/-/_ autorisés.',
                                max_length=150,
                                unique=False,
                                validators=[validate_unicode_slug],
                                verbose_name='username')
    REQUIRED_FIELDS = []


class Substitution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    substitution = models.ForeignKey(Product, related_name='substitution',
                                     on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'substitution_id')

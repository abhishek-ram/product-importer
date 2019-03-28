from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.SlugField(unique=True, max_length=150)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

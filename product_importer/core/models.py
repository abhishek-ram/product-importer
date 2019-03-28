from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.CharField(unique=True, max_length=150)
    description = models.TextField()
    active = models.BooleanField(default=True)

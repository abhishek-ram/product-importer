from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.SlugField(unique=True, max_length=150)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


def product_uploads_directory_path(instance, filename):
    return f'product_data/{timezone.now().strftime("%Y/%m/%d")}/' \
           f'{timezone.now().timestamp()}.csv'


class ProductUpload(models.Model):
    """ Model for managing the upload of product data """

    products_file = models.FileField(upload_to=product_uploads_directory_path)
    products_count = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


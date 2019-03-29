from django.db import models
from django.utils import timezone
from psqlextra.models import PostgresModel


class Product(PostgresModel):
    name = models.CharField(max_length=250)
    sku = models.SlugField(unique=True, max_length=150)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


def product_uploads_directory_path(instance, filename):
    return f'product_data/{timezone.now().strftime("%Y/%m/%d")}/' \
           f'{timezone.now().timestamp()}.csv'


class ProductUpload(PostgresModel):
    """ Model for managing the upload of product data """
    STATUS_CHOICES = (
        ('S', 'Successful'),
        ('F', 'Failed'),
    )

    products_file = models.FileField(
        upload_to=product_uploads_directory_path)
    products_count = models.IntegerField(default=0)

    task_id = models.CharField(max_length=100, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class EventHook(PostgresModel):
    """ Model for saving the web hooks for events """
    EVENT_CHOICES = (
        ('product.create', 'On Product Create'),
        ('product.update', 'On Product Update'),
    )

    event_type = models.CharField(max_length=100, choices=EVENT_CHOICES)
    endpoint = models.TextField()
    is_active = models.BooleanField(default=True)

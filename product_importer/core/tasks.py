import csv
import logging
import random
import traceback
from celery import shared_task
from django.utils import timezone
from psqlextra.query import ConflictAction

from product_importer.core.models import EventHook
from product_importer.core.models import ProductUpload
from product_importer.core.models import Product

logger = logging.getLogger('product-importer')


@shared_task
def import_products(product_upload_id):
    """ Task for import products from the CSV file"""
    product_upload = ProductUpload.objects.get(pk=product_upload_id)
    try:
        logger.info(f'Begin Product Import for upload {product_upload_id}')
        batch_size, total = 1000, 0
        rows, skus = [], set()
        with product_upload.products_file.open('r') as data_file:
            data_reader = csv.DictReader(data_file)

            for row in data_reader:
                if len(rows) <= batch_size:
                    if row['sku'] not in skus:
                        row['is_active'] = random.getrandbits(1)
                        skus.add(row['sku'])
                        rows.append(row)
                else:
                    total += batch_size
                    Product.objects \
                        .on_conflict(['sku'], ConflictAction.UPDATE) \
                        .bulk_insert(rows)
                    rows = []
            if rows:
                total += len(rows)
                Product.objects \
                    .on_conflict(['sku'], ConflictAction.UPDATE) \
                    .bulk_insert(rows)
        logger.info(f'Product Import for upload {product_upload_id} completed, '
                    f'{total} rows imported to the database.')
        product_upload.status = 'S'
    except Exception:
        logger.error(
            f'Product Import for upload {product_upload_id} failed '
            f'with error: {traceback.format_exc()}')
        product_upload.status = 'F'
        raise
    finally:
        product_upload.ended_at = timezone.now()
        product_upload.is_active = False
        product_upload.save()


@shared_task
def trigger_event_hooks(event_type, obj_id):
    """ Task for triggering event hooks"""
    obj, serializer_cls = None, None
    logger.info(f'Trigger event hook of type {event_type} for object {obj_id}')

    # Lookup the related object and serializer
    if event_type.startswith('product'):
        from product_importer.core.serializers import ProductSerializer

        obj = Product.objects.get(pk=obj_id)
        serializer_cls = ProductSerializer

    if obj and serializer_cls:
        post_data = {
            'event_type': event_type,
            'event_data': serializer_cls(obj).data
        }
        logger.info(f'Post data for this event is {post_data}')
        for event_hook in EventHook.objects.filter(
                event_type=event_type, is_active=True):
            logger.info(f'Posting the event data to webhook {event_hook.endpoint}')

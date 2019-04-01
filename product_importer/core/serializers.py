from rest_framework import serializers

from product_importer.core.models import ProductUpload
from product_importer.core.models import Product
from product_importer.core.tasks import import_products


class ProductUploadSerializer(serializers.ModelSerializer):
    """ Serializer for the Product upload Class """

    def create(self, validated_data):
        """ Override create to start async product import"""
        obj = super().create(validated_data)
        result = import_products.delay(obj.id)
        obj.task_id = result.task_id
        obj.save()
        return obj

    class Meta:
        model = ProductUpload
        fields = ('id', 'products_file')


class ProductSerializer(serializers.ModelSerializer):
    """ Serialize the product data """

    class Meta:
        model = Product
        fields = '__all__'

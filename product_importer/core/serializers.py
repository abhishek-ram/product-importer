from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from product_importer.core.models import ProductUpload


class ProductUploadSerializer(serializers.ModelSerializer):
    """ Serializer for the Product upload Class """
    products_file = serializers.FileField(
        validators=[FileExtensionValidator(['csv'])])

    def validate(self, data):
        """ Validate the upload of product data
        """
        if ProductUpload.objects.filter(is_active=True).exists():
            raise serializers.ValidationError(
                "Product Upload process is already running.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = ProductUpload
        fields = ('id', 'products_file')

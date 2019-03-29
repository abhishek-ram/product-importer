# Generated by Django 2.1.7 on 2019-03-28 07:28

from django.db import migrations, models
import product_importer.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190328_0710'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products_file', models.FileField(upload_to=product_importer.core.models.product_uploads_directory_path)),
                ('products_count', models.IntegerField(default=0)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
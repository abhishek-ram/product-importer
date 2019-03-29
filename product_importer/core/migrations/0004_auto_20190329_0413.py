# Generated by Django 2.1.7 on 2019-03-29 04:13

from django.db import migrations, models
import psqlextra.manager.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_productupload'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='productupload',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='productupload',
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.AddField(
            model_name='productupload',
            name='status',
            field=models.CharField(blank=True, choices=[('S', 'Successful'), ('F', 'Failed')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='productupload',
            name='task_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productupload',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
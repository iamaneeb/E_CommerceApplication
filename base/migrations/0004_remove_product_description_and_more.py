# Generated by Django 4.2.4 on 2023-09-10 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='product',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]

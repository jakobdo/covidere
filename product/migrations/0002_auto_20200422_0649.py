# Generated by Django 3.0.4 on 2020-04-22 06:49

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=stdimage.models.JPEGField(upload_to='images/%Y/%m/%d/', verbose_name='image'),
        ),
    ]

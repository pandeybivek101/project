# Generated by Django 2.1.7 on 2019-06-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20190607_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.TextField(),
        ),
    ]
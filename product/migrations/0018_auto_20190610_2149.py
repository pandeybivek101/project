# Generated by Django 2.1.7 on 2019-06-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20190610_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]

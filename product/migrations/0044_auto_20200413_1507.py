# Generated by Django 2.2.12 on 2020-04-13 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20200413_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_contact',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='show_location',
            field=models.BooleanField(default=True),
        ),
    ]
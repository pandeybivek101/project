# Generated by Django 2.1.7 on 2019-06-09 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_product_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catagory', models.CharField(max_length=100)),
            ],
        ),
    ]

# Generated by Django 2.1.7 on 2019-06-24 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0030_auto_20190624_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='repliedby',
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_user',
            field=models.ManyToManyField(null=True, related_name='replies', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 3.2.7 on 2021-09-11 21:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_auto_20210908_0804'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Event',
        ),
    ]

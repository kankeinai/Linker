# Generated by Django 3.2.7 on 2021-10-08 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_usersession'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
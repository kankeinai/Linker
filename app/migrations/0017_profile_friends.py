# Generated by Django 3.2.7 on 2021-10-07 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_event_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='_app_profile_friends_+', to='app.Profile'),
        ),
    ]

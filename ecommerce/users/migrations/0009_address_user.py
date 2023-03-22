# Generated by Django 4.0.10 on 2023-03-17 01:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_reset_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
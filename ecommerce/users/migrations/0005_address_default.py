# Generated by Django 4.0.10 on 2023-04-05 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_address_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]

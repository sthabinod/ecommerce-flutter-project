# Generated by Django 4.0.10 on 2023-04-06 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_address_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address',
            field=models.CharField(default=1, max_length=256),
            preserve_default=False,
        ),
    ]

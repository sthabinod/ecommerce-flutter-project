# Generated by Django 4.0.10 on 2023-03-12 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_verified_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_otp',
            field=models.CharField(default=1234, max_length=4),
            preserve_default=False,
        ),
    ]

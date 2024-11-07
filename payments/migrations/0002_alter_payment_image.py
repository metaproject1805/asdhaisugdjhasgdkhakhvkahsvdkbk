# Generated by Django 3.2.25 on 2024-11-07 11:13

import base.utils.validators
import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, validators=[base.utils.validators.file_validation], verbose_name='image'),
        ),
    ]
# Generated by Django 5.1.2 on 2024-10-25 06:46

import base.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=15)),
                ('image', models.ImageField(null=True, upload_to='payments', validators=[base.utils.validators.file_validation], verbose_name='image')),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
    ]

# Generated by Django 3.2.25 on 2024-12-29 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('movie', 'movie'), ('music', 'music'), ('thrillers', 'thrillers'), ('commercial advertisement', 'commercial advertisement'), ('football', 'football')], max_length=50)),
                ('file', models.URLField(default='')),
                ('watch_count', models.IntegerField(default=0)),
                ('total_watch', models.IntegerField(default=100)),
            ],
        ),
    ]

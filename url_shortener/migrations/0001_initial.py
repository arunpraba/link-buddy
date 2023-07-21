# Generated by Django 4.2.3 on 2023-07-21 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedURL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('original_url', models.URLField(unique=True)),
                ('short_code', models.CharField(max_length=10, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
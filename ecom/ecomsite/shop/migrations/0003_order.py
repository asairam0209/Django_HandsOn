# Generated by Django 5.1.4 on 2025-04-14 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_rename_products_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.CharField(max_length=1000)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('zip', models.CharField(max_length=100)),
            ],
        ),
    ]

# Generated by Django 5.1.4 on 2025-04-09 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TicketManager', '0006_alter_ticketmanager_clientid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authuser',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='TicketManager.rolemodel'),
        ),
    ]

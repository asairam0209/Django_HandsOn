# Generated by Django 5.0.7 on 2025-03-27 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TicketManager', '0002_rename_isprioriy_ticketmanager_ispriority_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketmanager',
            old_name='isPriority',
            new_name='i3_Priority',
        ),
    ]

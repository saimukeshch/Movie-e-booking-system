# Generated by Django 4.1.6 on 2023-04-18 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_rename_showtimeid_ticket_shownum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='showtimeID',
            new_name='shownum',
        ),
    ]

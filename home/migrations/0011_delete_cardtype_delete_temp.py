# Generated by Django 4.1.6 on 2023-04-21 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_rename_showtimeid_order_shownum'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CardType',
        ),
        migrations.DeleteModel(
            name='Temp',
        ),
    ]
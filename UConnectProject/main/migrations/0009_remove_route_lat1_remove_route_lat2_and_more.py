# Generated by Django 4.0.2 on 2022-05-03 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_route_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='lat1',
        ),
        migrations.RemoveField(
            model_name='route',
            name='lat2',
        ),
        migrations.RemoveField(
            model_name='route',
            name='long1',
        ),
        migrations.RemoveField(
            model_name='route',
            name='long2',
        ),
    ]

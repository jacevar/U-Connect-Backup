# Generated by Django 4.0.2 on 2022-03-17 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='lat1',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='route',
            name='lat2',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='route',
            name='long1',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='route',
            name='long2',
            field=models.FloatField(),
        ),
    ]

# Generated by Django 3.0.8 on 2020-10-24 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20201023_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='territoryitemmap',
            name='Price',
            field=models.FloatField(),
        ),
    ]

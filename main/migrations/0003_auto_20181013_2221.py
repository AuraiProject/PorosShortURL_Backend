# Generated by Django 2.1.2 on 2018-10-13 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20181013_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiredurl',
            name='created_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='url',
            name='created_time',
            field=models.IntegerField(),
        ),
    ]
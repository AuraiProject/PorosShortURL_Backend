# Generated by Django 2.1.2 on 2018-10-13 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiredurl',
            name='expired_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='expired_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
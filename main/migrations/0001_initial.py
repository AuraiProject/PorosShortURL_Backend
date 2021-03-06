# Generated by Django 2.1.2 on 2018-10-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiredUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(db_index=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expired_time', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(blank=True, max_length=16, null=True)),
                ('short_url', models.CharField(db_index=True, max_length=255)),
            ],
            options={
                'ordering': ('-created_time', 'short_url'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(db_index=True)),
                ('short_url', models.CharField(db_index=True, max_length=255, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('expired_time', models.DateTimeField(blank=True, null=True)),
                ('password', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'ordering': ('-created_time', 'short_url'),
                'abstract': False,
            },
        ),
    ]

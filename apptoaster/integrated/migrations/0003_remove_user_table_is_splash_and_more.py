# Generated by Django 4.1.5 on 2023-03-12 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('integrated', '0002_logger_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_table',
            name='is_splash',
        ),
        migrations.RemoveField(
            model_name='user_table',
            name='splash_min_time',
        ),
    ]
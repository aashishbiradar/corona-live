# Generated by Django 3.0.4 on 2020-03-28 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0003_daily'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daily',
            name='migrated',
        ),
    ]

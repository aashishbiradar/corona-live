# Generated by Django 3.0.4 on 2020-03-28 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corona', '0004_remove_daily_migrated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daily',
            name='id',
        ),
        migrations.AlterField(
            model_name='daily',
            name='date',
            field=models.DateField(primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-21 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_tickets_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='needs_repair',
        ),
        migrations.AddField(
            model_name='equipment',
            name='number_that_needs_repair',
            field=models.IntegerField(null=True),
        ),
    ]

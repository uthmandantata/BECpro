# Generated by Django 4.2.3 on 2023-07-31 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_duration_membership_duration_in_months'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='duration_period',
        ),
    ]
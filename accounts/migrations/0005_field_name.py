# Generated by Django 4.2.3 on 2023-07-31 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_field_bush_riding_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

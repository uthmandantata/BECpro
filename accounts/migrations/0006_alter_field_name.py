# Generated by Django 4.2.3 on 2023-07-31 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_field_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(default='dd', max_length=20, null=True),
        ),
    ]
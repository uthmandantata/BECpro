# Generated by Django 4.2.3 on 2023-08-19 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_membership_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('features', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='features',
            field=models.ManyToManyField(to='members.features'),
        ),
    ]

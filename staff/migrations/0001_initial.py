# Generated by Django 4.2.3 on 2023-08-21 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('amount', models.IntegerField(null=True)),
                ('price_bought', models.IntegerField(null=True)),
                ('needs_repair', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True)),
                ('riding_field_status', models.CharField(choices=[('Closed', 'Closed'), ('Open', 'Open')], max_length=20, null=True)),
                ('polo_field_status', models.CharField(choices=[('Closed', 'Closed'), ('Open', 'Open')], max_length=20, null=True)),
                ('bush_riding_status', models.CharField(choices=[('Closed', 'Closed'), ('Open', 'Open')], max_length=20, null=True)),
                ('riding_academy_status', models.CharField(choices=[('Closed', 'Closed'), ('Open', 'Open')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Horses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('age', models.IntegerField(null=True)),
                ('date_bought', models.DateField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('height', models.IntegerField(null=True)),
                ('for_polo', models.BooleanField(default=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True)),
                ('duration', models.CharField(max_length=150, null=True)),
                ('explanation', models.CharField(max_length=150, null=True)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('days', models.CharField(choices=[('Sunday', 'Sunday'), ('Friday', 'Friday'), ('Wednesday', 'Wednesday'), ('Saturday', 'Saturday')], max_length=200, null=True)),
                ('time_slot', models.CharField(choices=[('8-10 am', '8-10 am'), ('4-6 pm', '4-6 pm')], max_length=200, null=True)),
                ('amount', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(max_length=150, null=True)),
                ('attendant', models.CharField(max_length=150, null=True)),
                ('customer_fullname', models.CharField(max_length=150, null=True)),
                ('customer_email', models.CharField(max_length=150, null=True)),
                ('customer_number', models.CharField(max_length=150, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('total_price', models.CharField(max_length=150, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.services')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

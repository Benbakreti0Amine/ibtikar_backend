# Generated by Django 5.0.6 on 2024-12-15 01:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('report', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alert', to='report.report')),
            ],
        ),
    ]

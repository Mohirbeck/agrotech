# Generated by Django 4.2.1 on 2023-06-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrotech', '0002_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='companies'),
        ),
    ]
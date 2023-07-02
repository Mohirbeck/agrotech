# Generated by Django 4.2.1 on 2023-07-01 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agrotech', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

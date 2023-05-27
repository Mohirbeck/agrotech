# Generated by Django 4.2.1 on 2023-05-27 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agrotech', '0002_emailattempt_emailcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='agrotech.cartproduct'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='agrotech.product'),
        ),
    ]

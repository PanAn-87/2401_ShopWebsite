# Generated by Django 5.0 on 2024-01-04 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='items_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

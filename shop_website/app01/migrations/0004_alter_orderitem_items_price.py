# Generated by Django 5.0 on 2024-01-04 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_alter_cartitem_items_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='items_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0 on 2024-01-08 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_order_payment_alter_order_order_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
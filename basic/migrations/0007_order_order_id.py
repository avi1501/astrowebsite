# Generated by Django 3.2.5 on 2021-08-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_order_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
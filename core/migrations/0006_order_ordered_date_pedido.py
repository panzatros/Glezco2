# Generated by Django 3.0.7 on 2020-07-17 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200717_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered_date_pedido',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

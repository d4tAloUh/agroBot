# Generated by Django 4.2 on 2023-04-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_alter_product_options_product_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesplacement',
            name='vat',
            field=models.CharField(blank=True, choices=[('with', 'З ПДВ'), ('without', 'БЕЗ ПДВ')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='salesplacement',
            name='price_type',
            field=models.CharField(blank=True, choices=[('f1', 'Ф1'), ('f2', 'Ф2')], max_length=2, null=True),
        ),
    ]

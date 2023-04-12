# Generated by Django 4.2 on 2023-04-12 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_alter_city_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesplacement',
            name='status',
            field=models.CharField(choices=[('draft', 'DRAFT'), ('posted', 'POSTED')], default='draft', max_length=32),
            preserve_default=False,
        ),
    ]

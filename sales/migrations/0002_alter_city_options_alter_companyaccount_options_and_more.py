# Generated by Django 4.2 on 2023-04-10 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'City', 'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='companyaccount',
            options={'verbose_name': 'CompanyAccount', 'verbose_name_plural': 'Company accounts'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Region', 'verbose_name_plural': 'Regions'},
        ),
        migrations.AlterModelOptions(
            name='salesplacement',
            options={'verbose_name': 'Sale placement', 'verbose_name_plural': 'Sale Placements'},
        ),
        migrations.AlterModelOptions(
            name='subregion',
            options={'verbose_name': 'SubRegion', 'verbose_name_plural': 'SubRegions'},
        ),
        migrations.AlterField(
            model_name='city',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cities', related_query_name='city', to='sales.region'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='city',
            name='subregion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cities', related_query_name='city', to='sales.subregion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subregion',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subregions', related_query_name='subregion', to='sales.region'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.1.7 on 2021-05-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.BigIntegerField(default=None, unique=True)),
                ('name', models.CharField(default=None, max_length=100)),
                ('image_url', models.CharField(default=None, max_length=150)),
                ('quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('nutriscore', models.CharField(default=None, max_length=1)),
                ('energy_kcal_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fat_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('saturated_fat_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('carbohydrates_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sugars_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fiber_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('proteins_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salt_100g', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('energy_kcal_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('fat_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('saturated_fat_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('carbohydrates_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('sugars_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('fiber_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('proteins_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('salt_100g_unit', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('products', models.ManyToManyField(related_name='categories', to='search.Product')),
            ],
        ),
    ]
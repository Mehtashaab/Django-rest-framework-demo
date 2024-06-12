# Generated by Django 5.0.6 on 2024-05-30 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardekhoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carlist',
            name='chassisnumber',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='carlist',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]
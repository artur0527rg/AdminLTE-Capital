# Generated by Django 4.1.12 on 2024-02-01 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_company_link_remove_historicalcompany_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='number',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='historicalcompany',
            name='number',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]

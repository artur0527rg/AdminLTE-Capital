# Generated by Django 4.1.12 on 2024-03-05 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_fairvaluelist_historicalfairvaluemethod_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fairvaluemethod',
            unique_together={('company', 'fair_value_list')},
        ),
    ]

# Generated by Django 4.1.12 on 2024-02-18 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_historicalcompanyhouseparser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyhouseparser',
            name='shareholder_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.shareholderlist'),
        ),
        migrations.AlterField(
            model_name='historicalshareholder',
            name='option',
            field=models.BooleanField(default=True, verbose_name='Share'),
        ),
        migrations.AlterField(
            model_name='shareholder',
            name='option',
            field=models.BooleanField(default=True, verbose_name='Share'),
        ),
    ]

# Generated by Django 4.1.12 on 2024-03-01 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_fairvaluemethod_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fairvaluemethod',
            name='color',
            field=models.CharField(choices=[('#92d14f', 'Green'), ('#ffff00', 'Yellow'), ('#fe0000', 'Red'), ('#ffffff', 'White')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='historicalfairvaluemethod',
            name='color',
            field=models.CharField(choices=[('#92d14f', 'Green'), ('#ffff00', 'Yellow'), ('#fe0000', 'Red'), ('#ffffff', 'White')], max_length=8, null=True),
        ),
    ]

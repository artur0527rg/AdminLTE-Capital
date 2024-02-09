# Generated by Django 4.1.12 on 2024-02-09 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_company_number_alter_historicalcompany_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyHouseParser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_id', models.CharField(max_length=32)),
                ('date', models.DateField(auto_now_add=True)),
                ('comment', models.TextField(blank=True, max_length=10240)),
                ('status', models.BooleanField(default=False)),
                ('shareholder_list_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.share')),
            ],
            options={
                'verbose_name_plural': '12. Company House Parser',
                'db_table': 'company_house_parser',
            },
        ),
    ]

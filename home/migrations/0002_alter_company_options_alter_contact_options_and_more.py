# Generated by Django 4.1.12 on 2024-01-08 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['name'], 'verbose_name_plural': '2. Companys'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name_plural': '1. Contacts'},
        ),
        migrations.AlterModelOptions(
            name='historicalcompany',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical company', 'verbose_name_plural': 'historical 2. Companys'},
        ),
        migrations.AlterModelOptions(
            name='historicalcontact',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical contact', 'verbose_name_plural': 'historical 1. Contacts'},
        ),
        migrations.AlterModelOptions(
            name='historicalmoneytransaction',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical money transaction', 'verbose_name_plural': 'historical 4. Money Transactions'},
        ),
        migrations.AlterModelOptions(
            name='historicalseedstep',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical seed step', 'verbose_name_plural': 'historical 9. Seed Steps'},
        ),
        migrations.AlterModelOptions(
            name='historicalshare',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical share', 'verbose_name_plural': 'historical 3. Shares'},
        ),
        migrations.AlterModelOptions(
            name='historicalshareholder',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical shareholder', 'verbose_name_plural': 'historical 7. Shareholders'},
        ),
        migrations.AlterModelOptions(
            name='historicalshareprice',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical share price', 'verbose_name_plural': 'historical 6. Share Price'},
        ),
        migrations.AlterModelOptions(
            name='historicalsharetransaction',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical share transaction', 'verbose_name_plural': 'historical 5. Share Transaction'},
        ),
        migrations.AlterModelOptions(
            name='moneytransaction',
            options={'ordering': ['-date'], 'verbose_name_plural': '4. Money Transactions'},
        ),
        migrations.AlterModelOptions(
            name='seedstep',
            options={'ordering': ['-end_term'], 'verbose_name_plural': '9. Seed Steps'},
        ),
        migrations.AlterModelOptions(
            name='share',
            options={'verbose_name_plural': '3. Shares'},
        ),
        migrations.AlterModelOptions(
            name='shareholder',
            options={'verbose_name_plural': '7. Shareholders'},
        ),
        migrations.AlterModelOptions(
            name='shareprice',
            options={'verbose_name_plural': '6. Share Price'},
        ),
        migrations.AlterModelOptions(
            name='sharetransaction',
            options={'verbose_name_plural': '5. Share Transaction'},
        ),
        migrations.AlterModelOptions(
            name='split',
            options={'verbose_name_plural': '8. Splits'},
        ),
        migrations.AddField(
            model_name='split',
            name='comment',
            field=models.TextField(blank=True, max_length=10240),
        ),
    ]

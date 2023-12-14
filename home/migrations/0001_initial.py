# Generated by Django 4.1.12 on 2023-12-14 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('short_name', models.CharField(blank=True, max_length=256)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('link', models.CharField(blank=True, max_length=256)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_info.categoryofcompany')),
            ],
            options={
                'db_table': 'company',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=128)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('website', models.CharField(blank=True, max_length=256)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_info.contacttype')),
            ],
            options={
                'db_table': 'contact',
            },
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.company')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_info.sharetype')),
            ],
            options={
                'db_table': 'share',
                'unique_together': {('company', 'type')},
            },
        ),
        migrations.CreateModel(
            name='SharePrice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=8, max_digits=16)),
                ('date', models.DateField()),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.share')),
            ],
            options={
                'db_table': 'share_price',
            },
        ),
        migrations.CreateModel(
            name='Shareholder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('complite', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.contact')),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.share')),
            ],
            options={
                'db_table': 'shareholder',
            },
        ),
        migrations.CreateModel(
            name='SeedStep',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start_term', models.DateField()),
                ('end_term', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.company')),
            ],
            options={
                'db_table': 'seed_step',
                'ordering': ['-end_term'],
            },
        ),
        migrations.CreateModel(
            name='OurTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('amount', models.IntegerField(verbose_name='Amount of Shares')),
                ('price', models.DecimalField(decimal_places=8, max_digits=16, verbose_name='Price per 1 share')),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('share', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.share')),
            ],
            options={
                'db_table': 'our_transaction',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalSharePrice',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('price', models.DecimalField(decimal_places=8, max_digits=16)),
                ('date', models.DateField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('share', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.share')),
            ],
            options={
                'verbose_name': 'historical share price',
                'verbose_name_plural': 'historical share prices',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalShareholder',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('complite', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.contact')),
                ('share', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.share')),
            ],
            options={
                'verbose_name': 'historical shareholder',
                'verbose_name_plural': 'historical shareholders',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalShare',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.company')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base_info.sharetype')),
            ],
            options={
                'verbose_name': 'historical share',
                'verbose_name_plural': 'historical shares',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSeedStep',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('start_term', models.DateField()),
                ('end_term', models.DateField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.company')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical seed step',
                'verbose_name_plural': 'historical seed steps',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOurTransaction',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('date', models.DateField()),
                ('amount', models.IntegerField(verbose_name='Amount of Shares')),
                ('price', models.DecimalField(decimal_places=8, max_digits=16, verbose_name='Price per 1 share')),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('share', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.share')),
            ],
            options={
                'verbose_name': 'historical our transaction',
                'verbose_name_plural': 'historical our transactions',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContact',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=128)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('website', models.CharField(blank=True, max_length=256)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base_info.contacttype')),
            ],
            options={
                'verbose_name': 'historical contact',
                'verbose_name_plural': 'historical contacts',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCompany',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('short_name', models.CharField(blank=True, max_length=256)),
                ('comment', models.TextField(blank=True, max_length=1024)),
                ('link', models.CharField(blank=True, max_length=256)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base_info.categoryofcompany')),
                ('contact', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='home.contact')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base_info.location')),
                ('sector', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base_info.sector')),
                ('staff', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='base_info.companystatus')),
            ],
            options={
                'verbose_name': 'historical company',
                'verbose_name_plural': 'historical companys',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='home.contact'),
        ),
        migrations.AddField(
            model_name='company',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_info.location'),
        ),
        migrations.AddField(
            model_name='company',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_info.sector'),
        ),
        migrations.AddField(
            model_name='company',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_info.companystatus'),
        ),
    ]

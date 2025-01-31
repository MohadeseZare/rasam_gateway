# Generated by Django 3.2.14 on 2024-05-27 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0026_auto_20240526_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargeCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_addr', models.CharField(max_length=100)),
                ('position', models.CharField(default=None, max_length=10, null=True)),
                ('charge_start_time', models.DateTimeField()),
                ('charge_end_time', models.DateTimeField()),
                ('incomplete_end', models.BooleanField(db_index=True, default=False)),
                ('complete_status', models.BooleanField(db_index=True, default=True)),
                ('start_between_charge', models.CharField(db_index=True, max_length=50)),
                ('pin', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='logs.pin')),
                ('type_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logs.typedata')),
            ],
        ),
    ]

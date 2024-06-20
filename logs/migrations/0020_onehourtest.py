# Generated by Django 3.2.14 on 2023-03-27 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0019_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneHourTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_addr', models.CharField(max_length=100)),
                ('pin', models.CharField(max_length=10)),
                ('position', models.CharField(default=None, max_length=10, null=True)),
                ('sendDataTime', models.BigIntegerField()),
                ('data', models.FloatField(null=True)),
                ('diff_data', models.FloatField(default=0)),
                ('updated_at', models.DateTimeField()),
                ('type_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logs.typedata')),
            ],
        ),
    ]

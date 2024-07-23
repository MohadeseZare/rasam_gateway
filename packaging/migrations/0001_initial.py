# Generated by Django 3.2.14 on 2023-01-02 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('datatime', models.BigIntegerField()),
                ('degree1', models.IntegerField(default=0)),
                ('degree2', models.IntegerField(default=0)),
                ('degree3', models.IntegerField(default=0)),
                ('degree4', models.IntegerField(default=0)),
                ('degree5', models.IntegerField(default=0)),
                ('degree6', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PackagingLiveData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mac_addr', models.CharField(max_length=50)),
                ('datatime', models.BigIntegerField()),
                ('degree2', models.IntegerField()),
                ('degree3', models.IntegerField()),
                ('degree4', models.IntegerField()),
                ('degree5', models.IntegerField()),
                ('degree6', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PackagingLlogData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mac_addr', models.CharField(max_length=50)),
                ('datatime', models.BigIntegerField()),
                ('degree1', models.IntegerField()),
                ('degree2', models.IntegerField()),
                ('degree3', models.IntegerField()),
                ('degree4', models.IntegerField()),
                ('degree5', models.IntegerField()),
                ('degree6', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfAlarm',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('section', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('alarm_row', models.CharField(max_length=10)),
                ('mac_addr', models.CharField(max_length=50)),
                ('start_time', models.BigIntegerField()),
                ('end_time', models.BigIntegerField(null=True)),
                ('type_of_alarm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='packaging.typeofalarm')),
            ],
        ),
    ]

# Generated by Django 3.2.14 on 2022-08-03 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0008_auto_20211018_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('type_data', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='livedata',
            old_name='sensor_data',
            new_name='data',
        ),
        migrations.RenameField(
            model_name='logdata',
            old_name='sensor_data',
            new_name='data',
        ),
        migrations.AddField(
            model_name='livedata',
            name='type_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logs.typedata'),
        ),
        migrations.AddField(
            model_name='logdata',
            name='type_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logs.typedata'),
        ),
    ]

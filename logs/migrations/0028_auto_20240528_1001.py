# Generated by Django 3.2.14 on 2024-05-28 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0027_auto_20240521_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fifteenminflow',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='fiveminflow',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='lastoffline',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='livedata',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='logdata',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='onehourflow',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='oneminflow',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='rotation',
            name='pin',
        ),
        migrations.RemoveField(
            model_name='thirtyminflow',
            name='pin',
        ),
    ]

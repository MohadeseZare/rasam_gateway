# Generated by Django 3.2.14 on 2022-08-24 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0010_auto_20220806_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livedata',
            name='data',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='logdata',
            name='data',
            field=models.FloatField(null=True),
        ),
    ]

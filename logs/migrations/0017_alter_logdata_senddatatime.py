# Generated by Django 3.2.14 on 2022-10-29 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0016_alter_logdata_senddatatime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='sendDataTime',
            field=models.DateTimeField(),
        ),
    ]

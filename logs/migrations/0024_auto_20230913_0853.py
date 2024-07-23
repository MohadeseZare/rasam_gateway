# Generated by Django 3.2.14 on 2023-09-13 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0023_lastoffline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logdata',
            name='sendDataTime',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AddIndex(
            model_name='logdata',
            index=models.Index(fields=['sendDataTime'], name='logs_logdat_sendDat_9cddca_idx'),
        ),
    ]

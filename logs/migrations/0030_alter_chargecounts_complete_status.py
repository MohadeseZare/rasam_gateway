# Generated by Django 3.2.14 on 2024-06-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0029_auto_20240602_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargecounts',
            name='complete_status',
            field=models.BooleanField(db_index=True),
        ),
    ]

# Generated by Django 3.2.14 on 2024-05-21 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0025_auto_20230913_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('tag', models.IntegerField()),
            ],
        ),
    ]

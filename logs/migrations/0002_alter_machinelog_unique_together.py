# Generated by Django 5.1.7 on 2025-03-13 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='machinelog',
            unique_together=set(),
        ),
    ]

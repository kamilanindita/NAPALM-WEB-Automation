# Generated by Django 2.2.17 on 2021-05-19 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicebackup',
            old_name='ftp',
            new_name='filename',
        ),
        migrations.AlterField(
            model_name='devicebackup',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]

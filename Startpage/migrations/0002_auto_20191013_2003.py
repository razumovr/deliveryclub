# Generated by Django 2.2.4 on 2019-10-13 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Startpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='langing',
            name='complete',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='langing',
            name='end',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='langing',
            name='heshteg',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='langing',
            name='land',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='langing',
            name='start',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='langing',
            name='success',
            field=models.CharField(max_length=300),
        ),
    ]

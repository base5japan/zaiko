# Generated by Django 2.1.2 on 2019-07-06 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_table', '0004_auto_20190224_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nohin',
            name='memo',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='メモ'),
        ),
        migrations.AlterField(
            model_name='shohin',
            name='memo',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='メモ'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-21 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_table', '0007_auto_20190706_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nohindetail',
            name='kataban',
            field=models.CharField(max_length=50, verbose_name='会社名'),
        ),
        migrations.AlterField(
            model_name='shohin',
            name='kataban',
            field=models.CharField(max_length=50, verbose_name='会社名'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-06-05 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(max_length=20, null=True, verbose_name='تصویر اواتار'),
        ),
    ]

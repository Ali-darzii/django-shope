# Generated by Django 4.1.7 on 2023-06-11 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_slider_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='url_title',
            field=models.URLField(verbose_name='عنوان لینک'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-06-11 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال/غیر فعال بودن'),
        ),
        migrations.AlterField(
            model_name='articlecategory',
            name='title',
            field=models.CharField(max_length=200, verbose_name='عنوان دسته بندی'),
        ),
        migrations.AlterField(
            model_name='articlecategory',
            name='url_title',
            field=models.CharField(max_length=500, verbose_name='عنوان در url'),
        ),
    ]
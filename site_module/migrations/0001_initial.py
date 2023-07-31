# Generated by Django 4.1.7 on 2023-06-10 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=200, verbose_name='نام سایت')),
                ('address', models.CharField(max_length=200, verbose_name='ادرس سایت')),
                ('phone', models.CharField(blank=True, max_length=200, null=True, verbose_name='تلفن سایت')),
                ('fax', models.CharField(blank=True, max_length=200, null=True, verbose_name='فکس سایت')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='ایمیل سایت')),
                ('copy_right', models.TextField(verbose_name='کپی رایت سایت')),
                ('site_logo', models.ImageField(upload_to='images/site_setting/', verbose_name='لوگو سایت')),
                ('site_url', models.CharField(max_length=200, verbose_name='دامنه سایت')),
                ('about_us_text', models.TextField(max_length=200, verbose_name='متن دریاره ما سایت')),
                ('is_main_setting', models.BooleanField(verbose_name='تنظیمات اصلی')),
            ],
            options={
                'verbose_name': 'تنظیمات سایت',
                'verbose_name_plural': 'تنظیمات',
            },
        ),
    ]

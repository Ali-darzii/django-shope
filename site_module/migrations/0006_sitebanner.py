# Generated by Django 4.1.7 on 2023-06-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0005_alter_slider_url_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان بنر')),
                ('url', models.URLField(blank=True, max_length=400, null=True, verbose_name='ادرس بنر')),
                ('image', models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')),
                ('is_active', models.BooleanField(verbose_name='فعال/غیرفعال بودن')),
                ('position', models.CharField(choices=[('product_list', 'صفحه لیست محصولات'), ('product_detail', 'صفحه جزییات محصولات'), ('about_us', 'درباره ما')], max_length=200, verbose_name='جایگاه نمایشی')),
            ],
            options={
                'verbose_name': 'بنر تبلیغاتی',
                'verbose_name_plural': 'بنرهای تبلیغاتی',
            },
        ),
    ]

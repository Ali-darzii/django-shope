from django.db import models


class SiteBanner(models.Model):
    class SiteBannerPositions(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail','صفحه جزییات محصولات'
        about_us = 'about_us','درباره ما'

    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(max_length=400, verbose_name='ادرس بنر', null=True, blank=True)
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال بودن')
    position = models.CharField(max_length=200, choices=SiteBannerPositions.choices, verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    address = models.CharField(max_length=200, verbose_name='ادرس سایت')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن ')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس ')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل ')
    copy_right = models.TextField(verbose_name='کپی رایت سایت')
    site_logo = models.ImageField(upload_to='images/site_setting/', verbose_name='لوگو سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    about_us_text = models.TextField(max_length=200, verbose_name='متن دریاره ما سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    footer_link_box = models.ForeignKey(FooterLinkBox, verbose_name='دسته بندی', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک های فوتر'
        verbose_name_plural = 'لینک های فوتر'


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    url = models.URLField(max_length=200, verbose_name='لینک')
    image = models.ImageField(upload_to='images/sliders', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    def __str__(self):
        return self.title

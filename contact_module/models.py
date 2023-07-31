from django.db import models


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='پیام متن')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد ', auto_now_add=True)
    response = models.TextField(verbose_name='متن پاسخ تماس با ما', null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'


class UserProfile(models.Model):
    image = models.ImageField(upload_to='images', verbose_name='عکس کاربر')
                    # image filed only works with pillow package
    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل های کاربر'

    # def __str__(self):
    #     return self.image.path


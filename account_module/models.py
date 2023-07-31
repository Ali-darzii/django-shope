from django.db import models

from django.contrib.auth.models import AbstractUser, AbstractBaseUser


# in AbstractBaseUser we have nothing, and we write the whole auth-user from beginning, and it's
# not recommended
# in AbstractUser we have default django auth_user


# with this class we can say plus that things exist in django default (auth-user) we need these things too in our DB
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile', verbose_name='تصویر اواتار', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعال سازی ایمیل')
    about_user = models.TextField(null=True, blank=True, verbose_name='درباره نویسنده')
    address = models.TextField(null=True, blank=True, verbose_name='ادرس')

    # confirm_password = models.CharField(max_length=100, verbose_name='تایید رمز')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email

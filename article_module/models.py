from django.db import models

from django.urls import reverse
from jalali_date import date2jalali
from django.contrib.auth import get_user_model
# Create your models here.
from account_module.models import User


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=500, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیر فعال بودن')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    # allow_unicode is for persian language
    image = models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = models.TextField(verbose_name='متن مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال بودن')
    selected_categories = models.ManyToManyField('ArticleCategory', verbose_name='دسته بندی ها')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', null=True, editable=False)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریح ثبت')

    # we are using django-jalali-date package for create_date in Article Class

    def get_absolute_url_article(self):
        return reverse('articles_detail', args=[self.slug])

    def __str__(self):
        return self.title

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class Comment(models.Model):
    CommentPost = models.ForeignKey('Article', on_delete=models.CASCADE, verbose_name='نظر پست', )
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='نویسنده')
    content = models.TextField(verbose_name='نظر')
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies',
                               verbose_name='ریپلای')

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'نظرات'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return str(self.CommentPost)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



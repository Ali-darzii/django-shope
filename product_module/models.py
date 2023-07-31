from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from account_module.models import User


# from django.utils.text import slugify

class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=200, unique=True, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال/غیر فعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    urls_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(
        ProductCategory,
        related_name="product_categories",
        verbose_name='دسته بندی ها')  # CASCADE means when we have 5
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    # product and one category when category deleted products going to be deleted too and against this we have protect
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    # rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
    #                              default=0, )  # django models validators
    short_descriptions = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    descriptions = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    is_active = models.BooleanField(default=False,
                                    verbose_name='فعال/غیر فعال')  # for filter in django we have (rating__lt ==
    # lower than and __gt
    # greater than, so we can use rating__lte ,e stands for Equal
    #  django Query duc looking up
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def get_absolute_url(self):  # or it can be args=[self.id]
        return reverse('product-detail', args=[self.slug])

    # this def do exact the {{url 'product-detail' product_id=product.id}} in html
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)  # we write this to every time add a data to database automatically made a
        # slug by title
        super().save(*args, **kwargs)  # this is the default, and we don't want to change this,so we should overwrite it

    def __str__(self):
        return f"{self.title} "

    class Meta:
        verbose_name = "محصول"  # with this we can show the name of this class in admin panel
        verbose_name_plural = "محصولات"


class ProductTag(models.Model):
    caption = models.CharField(max_length=200, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_tags',
                                verbose_name='تگ محصول')

    class Meta:
        verbose_name = "تگ محصول"
        verbose_name_plural = "تگ های محصولات"

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='ای پی کابر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربری که مشاهده کرده',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} / {self.ip}"

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر محصولات')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'

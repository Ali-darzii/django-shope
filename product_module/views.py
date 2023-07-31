from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, View

from site_module.models import SiteBanner
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery
from django.http import Http404, HttpRequest
from django.db.models import Avg, Count
from utils.http_service import get_client_ip
from utils.convertors import group_list


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product  # it's going to discover the model
    context_object_name = 'product'  # with this we set name for model
    ordering = ['-price']
    paginate_by = 6  # it tells that in every page how many items do you want me to show

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context


    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')

        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        if category_name is not None:
            query = query.filter(category__urls_title__iexact=category_name)
        # category_url = self.kwargs.get('category-product')
        # if category_url is not None:
        #     data = data.filter(category__urls_title__iexact=category_url)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        product_gallery = list(ProductGallery.objects.filter(product_id=self.object.id).all())
        product_gallery.insert(0,self.object)
        context['product_galleries_group'] = group_list(product_gallery,3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=self.object.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit.objects.create(ip=user_ip, user_id=user_id, product_id=self.object.id)
            new_visit.save()
        brand_products = list(Product.objects.filter(brand_id=self.object.brand_id).exclude(pk=self.object.id).all()[:12])
        context['related_products'] = group_list(brand_products,3)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     loaded_product = self.object  # it's get the object that we send to html = product
    #     request = self.request
    #     favorite_product_id = request.session['product_favorite']
    #     context['is_favorite'] = favorite_product_id == str(loaded_product.id)

    # return context
    # with DetailVew we don't need to send slug or id it's going to find out
    # with it self in DetailView we don't need
    # to send the contex for little stuffs like
    # ListView but for else like category or brand we should and for
    # example like end of the page suggest products


class AddProductFavorite(View):  # View make effect on all templates
    def post(self, request):
        product_id = request.POST["mostafa_online"]  # with name of input(product_name)
        # we found the which input and from that we get the product id

        request.session["product_favorite"] = product_id  # we send the pk to Session not the whole product
        # every name it can be
        product = Product.objects.get(pk=product_id)  # we need this for redirect
        return redirect(product.get_absolute_url())


def product_categories_component(request: HttpRequest):
    product_categories: ProductCategory = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'product_categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_components.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True)
    # product_brands.product_set.count()  #not good way because it will get 100 query
    context = {
        'brands': product_brands
    }

    return render(request, 'product_module/components/product_brands_component.html', context)

# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         products = Product.objects.all().order_by('-price')
#         context = super(ProductListView, self).get_context_data()
#         context['products'] = products
#         return context


# def product_list(request):
#     products = Product.objects.all().order_by('-price')
#     numbers_of_products = products.count()
# context = {
#     "products": products,
#     'total_number_of_products': numbers_of_products,
# }
# return render(request, 'product_module/product_list.html', context)


# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data()
#         slug = kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         context['product'] = product
#         return context

# def product_detail(request, slug):
# try:
#     products = Product.objects.get(id=product_id)
# except:
#     raise Http404
# products = get_object_or_404(Product, slug=slug)

# return render(request, 'product_module/product_detail.html', {
#     'product': products
# })

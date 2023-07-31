from django.db.models import Count, Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list


# class HomeView(View):
#     def get(self, request):
#         return render(request, 'index_page.html')

class HomeView(TemplateView):  # for get method we will use this (it's better)
    template_name = 'index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs)  # if we didn't have context we must write instead of context = --> return
        slider: Slider = Slider.objects.filter(is_active=True)
        context['sliders'] = slider

        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[
                          :8]  # == 12 new products
        context['latest_products'] = group_list(latest_products)

        most_visited_products = Product.objects.filter(is_delete=False, is_active=True).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:8]
        context['most_visit'] = group_list(most_visited_products)

        categories = list(
            ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(is_delete=False,
                                                                                                is_active=True,
                                                                                                product_categories__gt=0)[
            :6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all())
            }
            categories_products.append(item)

        context['categories_products'] = categories_products

        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]

        context['most_bought_products'] = group_list(most_bought_products)
        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {'site_setting': setting}
    return render(request, 'shared/site_header_component.html', context)
    # we don't set url for header or footer because we don't need it


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes: FooterLinkBox = FooterLinkBox.objects.all()

    context = {
        'site_setting': setting,
        'footer_link_box': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView, ):
    template_name = 'about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context

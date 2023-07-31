from . import views
from django.urls import path

urlpatterns = [

    # path('', views.product_list, name='product-list'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('cat/<str:cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<str:brand>', views.ProductListView.as_view(), name='product_by_brand_list'),
    # path('<slug:slug>/', views.product_detail, name='product-detail')
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    # we can use int:pk or slug:slug for class(DetailView) --> in views
    path('product-favorite', views.AddProductFavorite.as_view(), name='product-favorite')
]

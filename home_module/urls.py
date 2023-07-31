from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-page'),
    # path('site-header', views.site_header_partial, name='site-header-partial'),
    path('about-us/', views.AboutView.as_view(), name='about_page'),
]

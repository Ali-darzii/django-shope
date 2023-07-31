from . import views
from django.urls import path

urlpatterns = [

    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('edit-profile', views.EditUserPage.as_view(), name='edit_user_page'),
    path('change-pass', views.ChangPasswordPage.as_view(), name='change_password_page'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count, name='change_order_detail_ajax'),
    path('my-shoppings', views.MySHopping.as_view(), name='my_shopping_pages'),


]

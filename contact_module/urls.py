from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.contact_us_page, name='contact_us_page'),
    path('', views.ContactUsView.as_view(), name='contact_us_page'),
    path('create-profile/', views.CreateProfileView.as_view(), name='create_profile_page'),
    path('profile-list/', views.ProfileView.as_view(), name='profile_list_page')
]

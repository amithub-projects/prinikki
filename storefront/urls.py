from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('announcements/', views.announcement_list, name='announcements'),
    path('announcements/<slug:slug>/', views.announcement_detail, name='announcement_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

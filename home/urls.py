from django.urls import path

from home import views
urlpatterns = [
    path('', views.index, name='index'),
    path('lien-he/', views.contact, name='contact'),
    path('cau-hoi-thuong-gap/', views.qfa, name='qfa'),
    path('ve-chung-toi/', views.abous, name='abous'),
    path('danh-muc-san-pham/<int:id>/<slug:slug>', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
]
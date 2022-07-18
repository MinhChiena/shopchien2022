from django.urls import path

from product import views

urlpatterns = [
    path('', views.product, name='product'),
    path('<int:id>/<slug:slug>', views.products_detail, name='products_detail'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('list/', views.list, name='list')
]
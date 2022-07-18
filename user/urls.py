from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('order/', views.user_order, name='user_order'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
]
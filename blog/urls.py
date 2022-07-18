from django.urls import path

from blog import views
urlpatterns = [
    path('', views.index1, name='index1'),
    path('<int:id>/<slug:slug>', views.blog_detail, name='blog_detail'),
    path('category_blog/<int:id>/<slug:slug>/', views.categoryblog1, name='categoryblog1'),
]
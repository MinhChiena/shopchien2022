"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from order import views as OrderViews
from user import views as UserViews

urlpatterns = [
    path('ncb', admin.site.urls),
    path('', include('home.urls')),
    path('tin-tuc/', include('blog.urls')),
    path('order/', include('order.urls')),
    path('san-pham/', include('product.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('gio-hang/', OrderViews.shopcart, name='shopcart'),
    path('user/', include('user.urls'), name='user'),
    path('login/', UserViews.login_form, name='login_form'),
    path('logout/', UserViews.logout_func, name='logout_func'),
    path('dang-ky/', UserViews.sinup_form, name='sinup_form'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
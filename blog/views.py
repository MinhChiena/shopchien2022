from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from blog.models import Blog_Home, Category_blog
from order.models import ShopCart
from product.models import Images


def index1(request,page1=1):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    categoryblog = Category_blog.objects.all()
    blog = Blog_Home.objects.all()

    paginator = Paginator(blog, 6)
    page_num = request.GET.get('page', 1)
    try:
        blog = paginator.page(page_num)
    except InvalidPage:
        # if the page contains no results (EmptyPage exception) or
        # the page number is not an integer (PageNotAnInteger exception)
        # return the first page
        blog = paginator.page(1)
    context = {
        'blog': blog,
        'categoryblog': categoryblog,
        'shopcart':shopcart,
    }
    return render(request, 'blog/blog_home.html', context)


def blog_detail(request,id,slug):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    catelory_blog = Category_blog.objects.all()
    blog1 = Blog_Home.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context = {
        'catelory_blog':catelory_blog,
        'blog1':blog1,
        'images':images,
        'shopcart':shopcart,
    }
    return render(request, 'blog/blog_title.html', context)


def categoryblog1(request, id, slug):
    category = Category_blog.objects.all()
    list_blog = Blog_Home.objects.filter(category_id=id)
    # list_blog = Blog_Home.objects.all()
    # paginator = Paginator(list_blog, 3)
    # page_num = request.GET.get('page', 1)
    # try:
    #     list_blog = paginator.page(page_num)
    # except InvalidPage:
    #     list_blog = paginator.page(1)
    context = {
        'category': category,
        'list_blog': list_blog,
    }
    return render(request, 'blog/category_blog.html', context)
from django.contrib import messages
from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
from order.models import ShopCart
from product.models import Product, Category, Images, CommentForm, Comment, Images1


def product(request,page=1):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    nhat = Product.objects.all()
    category = Category.objects.all()
    # list-nhat = Product.buildpart.all().order_by('family__type')

    product = Product.objects.all()

    paginator = Paginator(product, 6)
    page_num = request.GET.get('page', 1)
    try:
        product = paginator.page(page_num)
    except InvalidPage:
        # if the page contains no results (EmptyPage exception) or
        # the page number is not an integer (PageNotAnInteger exception)
        # return the first page
        product = paginator.page(1)
    # p = Paginator(product, 3)
    # print('number page')
    # print(p.num_pages)
    # page_num = request.GET.get('page',1)
    # try:
    #     page =p.page(page_num)
    # except EmptyPage:
    #     page = p.page(1)
    context={
        # 'nhat': nhat,
        'category': category,
        'product': product,
        'shopcart': shopcart,
    }
    return render(request, 'product/product.html', context)


def products_detail(request,id,slug):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    images1 = Images1.objects.filter(product_id=id, product__images1=id)
    relate_product = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
        # 'images1': images1,
        'relate_product':relate_product,
        'shopcart':shopcart,


    }
    return render(request, 'product/produc_detail.html', context)


def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    # return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            data = Comment()  # create relation with model
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.image = form.cleaned_data['image']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "cám ơn bạn đã đánh giá sản phẩm.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)


def list(request):
    nhat = Product.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    paginator = Paginator(product, 2)
    page = request.GET.get('page', 1)
    # ?page = 2
    product = paginator.get_page(page)
    context = {
        'nhat': nhat,
        'category': category,
        'product': product,
    }
    return render(request, 'product/list.html', context)
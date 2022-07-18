import json

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import ContactForm, ContactMessage
from order.models import ShopCart
from product.models import Category, Product


def index(request):
    category = Category.objects.all()
    product = Product.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    products_slider = Product.objects.all().order_by('id')[:5]
    context={
        'category': category,
        'product':product,
        'products_slider':products_slider,
        'shopcart':shopcart,
    }
    return render(request, 'home/index.html', context)


def contact(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    if request.method == 'POST':
        form = ContactForm(request.POST)  # check post
        if form.is_valid():
            data = ContactMessage()  # create relation with model
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save dato to table
            messages.success(request, "you message has send. thanks for you")
            return HttpResponseRedirect('/lien-he')

    form = ContactForm
    context = {'form': form, 'shopcart': shopcart,}
    return render(request, 'home/contact.html', context)


def category(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context={
        'category':category,
        'products':products,
    }
    return render(request, 'product/catology.html', context)


def search(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    form = SearchForm(request.POST)
    if form.is_valid():
        query = form.cleaned_data['query']  # get form input data
        catid = form.cleaned_data['catid']
        if catid == 0:
            products = Product.objects.filter(
                title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
        else:
            products = Product.objects.filter(title__icontains=query, category_id=catid)

        category = Category.objects.all()
        context = {'products': products, 'query': query,
                   'category': category, 'shopcart':shopcart,}
        return render(request, 'product/search.html', context)
    return HttpResponseRedirect('/')
    # return render(request, 'product/search.html')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def qfa(request):
    return render(request, 'home/fqa.html')


def abous(request):
    return render(request, 'home/abous.html')
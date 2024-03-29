from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string
# Create your views here.
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product
from user.models import UserProfile


def index(request):
    return HttpResponse("hello")


@login_required(login_url='/login') # Check login
def addtoshopcart(request,id):
    # return HttpResponse(str(id))
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information

    checkproduct = ShopCart.objects.filter(product_id=id)

    if checkproduct:
        control = 1  # The product is in the cart
    else:
        control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else:  # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                # data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Sản phẩm đã thêm vào giỏ hàng ")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Sản phẩm đã thêm vào giỏ hàng")
        return HttpResponseRedirect(url)


def shopcart(request):
    product = Product.objects.all()
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'product': product,
               }
    return render(request, 'order/shopcart_product.html', context)


def deletefromcart(request, id):
    nhat = ShopCart.objects.filter(id=id)
    nhat.delete()
    messages.success(request, "Bạn đã xóa một sản phẩm!")
    return HttpResponseRedirect("/gio-hang")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    shopcart1 = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    total = 0
    for rs in shopcart1:
        total += rs.product.price * rs.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(15).upper()  # random cod
            data.code = ordercode
            data.save()  #

            for rs in shopcart1:
                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "bạn đã đặt hàng thành công. ")
            return render(request, 'order/Order_Completed.html'
                                   '', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context ={
        'category': category,
        'current_user': current_user,
        'shopcart1': shopcart1,
        'total': total,
        'profile': profile,
        'shopcart':shopcart,

    }
    return render(request, 'order/order_product.html',context)
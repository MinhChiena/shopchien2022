from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
# Create your views here.
from order.models import Order, OrderProduct, ShopCart
from product.models import Category, Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


def login_form(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            messages.warning(request, "Đăng nhập thành công về trang chủ")
        else:
            messages.warning(request, "Lỗi đăng nhập & hãy điền user vs password")
            return HttpResponseRedirect("/login")

    category = Category.objects.all()
    context = {'category': category}
    return render(request, 'user/login_form.html', context)


def logout_func(request):
    logout(request)
    return HttpResponseRedirect("/")


def sinup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "static/img/brand-1.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/dang-ky')

    form = SignUpForm()
    # category = Category.objects.all()
    context = {  # 'category': category,
        'form': form,
    }
    return render(request, 'user/sinup_form.html', context)


@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user/user_update.html', context)


@login_required(login_url='/login') # Check login
def user_password(request):
    # return HttpResponse("update pass")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user/user_pasword.html', {'form': form,#'category': category
                       })

@login_required(login_url='/login') # Check login
def user_order(request):
    # category = Category.objects.all()
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context = {  # 'category': category,
        'orders': orders,
    }
    # return HttpResponse("order")
    return render(request,'user/user_order.html', context)

def index(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    comments = Comment.objects.filter(user_id=current_user.id)
    orders = Order.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               'comments': comments,
               'orders': orders,
               'shopcart':shopcart,
               }
    return render(request, 'user/user_profile.html',context)


@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    total1 = 0
    for rs in orderitems:
         total1 += rs.product.price * rs.quantity
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
        'total1': total1,
    }
    return render(request, 'user/user_orderdetail.html', context)


def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return render(request, 'user/user_profile.html')
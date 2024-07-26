from django.shortcuts import render,HttpResponse,redirect
from gamestopapp.models import product, cart, orders,Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,'index.html')

def create_Product(request):
    if request.method == "GET":
        return render(request,'create_product.html')
    
    else:
        name = request.POST['name']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES['image']
        
        p = product.objects.create(name = name, description = description, manufacturer = manufacturer, category =  category, price = price , image = image)
        p.save()
        return redirect('/')
    
def read_product(request):
    if request.method == "GET":
            
        P = product.objects.all()
        context = {'data': P}
        return render(request,'read_product.html',context)
    
    else:
        name = request.POST['search']
        prod = product.objects.get(name = name)
        return redirect(f'read_product_detail/{prod.id}')


def update_product(request,rid):
    if request.method == "GET":
        P = product.objects.filter(id = rid)
        context = {"Udata": P}
        return render(request,'update_product.html',context)
    
    else:
        name = request.POST['Uname']
        description = request.POST['Udescription']
        manufacturer = request.POST['Umanufacturer']
        category = request.POST['Ucategory']
        price = request.POST['Uprice']
        image = request.FILES['Uimage']
        
        p = product.objects.filter(id = rid )
        p.update(name = name, description = description, manufacturer = manufacturer, category =  category, price = price , image = image)
        return redirect('/read_Product')
    
def delete_Product(request, rid):
    di = product.objects.get(id = rid)
    di.delete()
    return redirect('/read_Product')


def user_register(request):
    if request.method == "GET":
        return render(request,'register.html')
    
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password :
            u = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email)
            u.set_password(password)
            u.save()
            return redirect('/login')
        
        else:
            context = {'error':'Password are not match' }
            
            return render(request, 'register.html',context)
        

def user_login(request):
    if request.method == "GET":
        
        return render(request,'login.html')
    
    else:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request,user)
            return redirect('/')
        
        else:
            context = {'error':'Username and Password is Incorrect'}
            return render(request,'login.html',context)
        
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def create_cart(request,rid):
    
    prod = product.objects.get(id = rid)
    cart_ = cart.objects.filter(product = prod, user = request.user).exists()
    if cart_:
        return redirect('/readCart')
    
    else:
        
        user = User.objects.get(username = request.user)
        total_price = prod.price
        
        c = cart.objects.create(product = prod, user = user, quantity = 1, total_price = total_price)
        c.save()
        return redirect('/readCart')


@login_required(login_url='/login')
def read_cart(request):
    
    c =cart.objects.filter(user = request.user)
    context = {'data': c}
    total_price = 0
    total_quantity = 0
    
    
    for x in c:
        total_quantity += x.quantity
        total_price += x.total_price
        
    context['total_quantity'] = total_quantity
    context['total_price'] = total_price
    return render(request,'read_cart.html',context)

def update_cart(request, rid, q): # q = quantity 
    C = cart.objects.filter(id = rid)
    c = cart.objects.get(id = rid )
    P = int(c.product.price) * int(q) # to calculate total price 
    C.update(quantity = q, total_price = P )
    
    return redirect('/readCart')

def delete_cart(request,rid):
    c = cart.objects.filter(id = rid)
    c.delete()
    return redirect('/readCart')

def create_orders(request, rid):
    c = cart.objects.get(id = rid)
    order = orders.objects.create(product = c.product, user = request.user, quantity = c.quantity, total_price = c.total_price)
    order.save()
    c.delete()
    
    return redirect('/readCart')    


def read_orders(request):
    order = orders.objects.filter(user = request.user)
    context = {'data': order}
    return render(request, 'read_order.html', context)

def create_review(request, rid):
    prod = product.objects.get(id = rid)
    rev = Review.objects.filter(user = request.user, product = prod)
    
    if rev:
        return HttpResponse('Review Already added')
    else:
        if request.method == "GET":
            return render(request, 'create_review.html')
        
        else:
            title = request.POST['title']
            content = request.POST['content']
            rating = request.POST['rate']
            image = request.FILES['image']
            
            
            p = product.objects.get(id = rid)
            review = Review.objects.create(product = p , user = request.user ,title = title, content = content, rating = rating, image = image)
            review.save()
            return HttpResponse("Review Save")
        
def read_product_detail(request, rid):
    prod = product.objects.filter(id = rid )
    p = product.objects.get(id = rid )
    n = Review.objects.filter(product = p).count()
    rev = Review.objects.filter(product = p)
    sum = 0
    for x in rev:
        sum += x.rating 
    
    try:    
        avg_r  = sum / n 
        avg = int(sum/n)
    except:
        print("No Review")
        
        
    context = {}
    context['data'] = prod 
    
    if n == 0:
        context['avg'] = 'No Review'
    else:
        context['avg_rating'] = avg 
        
        context['avg'] = avg_r 
       
    return render(request, 'readProductDetail.html',context)



def forget_password(request):
    if request.method == "GET":
        
        return render(request,'forgetpassword.html')
    
    else:
        email = request.POST['email']
        request.session['email'] = email
        user = User.objects.filter(email = email).exists()
        
        if user:
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS
            ) as connection:
                subject = 'Email from django project'
                message =  f'OTP {otp}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [email]
                
                EmailMessage(subject, message,from_email,recipient_list, connection= connection).send()
                return redirect('/otpVerification')
            
        else:
            context={}
            context['error']= 'Email dose not exists'
            return render(request, 'forgetpassword.html',context)
        
def otp_verification(request):
    if request.method == "GET":
        
        return render(request,'otpverification.html')
    else:
        otp = int(request.POST['otp'])
        otp_email = int(request.session['otp'])
        
        if otp == otp_email:
           return redirect('/reset_password')
            
        else:
           return HttpResponse('Not Ok')
       
       
def reset_password(request):
    if request.method == "GET":
        return render(request, 'newPassword.html')
    
    else:
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        email = request.session['email']
        user = User.objects.get(email = email)
        
        if password == confirm_password:
            user.set_password(password)
            user.save()
            return redirect('/login')
        
        else:
            context= {'error': "Password dose not match"}
            
            return render(request, 'newPassword.html', context)
                    
                    
# Search product

def search_product(request):
    if request.method == "GET":
        
        return render(request,'search_product.html')
    else:
        search = request.POST['search']
        
        prod = product.objects.filter(name = search)
        
        context = {}
        context['data'] = prod
        return render(request,'search_product.html',context)
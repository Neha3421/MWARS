from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from user.models import *

def index(request):
    return render(request, 'index.html')

def home(request):
    return index(request)

def adminlogin(request):
    return render(request, 'adminlogin.html')

def adminloginaction(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        paswd = request.POST.get('pswad')
        if name =='admin' and paswd =='admin' or name == 'Admin' and paswd=='Admin':
            data = Usermodel.objects.all()
            return render(request, 'admin/adminhome.html', {'data': data})
        else:
            messages.success(request, 'Incorrect Details')
            return render(request, 'adminlogin.html')
    else: 
        return render(request, 'adminlogin.html')

def adminhome(request):
    data = Usermodel.objects.all()
    return render(request, 'admin/adminhome.html', {'data': data})

def AdminActiveUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        Usermodel.objects.filter(id=id).update(status=status)
        data = Usermodel.objects.all()
        return render(request, "admin/adminhome.html", {'data': data})
    
def advertisementpage(request):
    data = advertisementmodel.objects.all()
    return render(request, 'admin/advertisementpage.html', {'data': data})

def uploadadd(request):
    if request.method =='POST':
        name = request.POST.get('name')
        image = request.FILES['image']
        addcat = request.POST.get('dropdown1')
        post_url = request.POST.get('url')
        form = advertisementmodel(name=name, image=image, addcat=addcat, post_url=post_url)
        form.save()
        return advertisementpage(request)
    else:
        return render(request, 'admin/advertisementpage.html')

def adminlogout(request):
    return adminlogin(request)

def addproduct(request):
    clothing_products = productmodel.objects.filter(addcat='Clothing').order_by('-id')[:5]
    electronics_products = productmodel.objects.filter(addcat='Electronics').order_by('-id')[:5]
    homegoods_products = productmodel.objects.filter(addcat='Homegoods').order_by('-id')[:5]

    context = {
        'clothing_products': clothing_products,
        'electronics_products': electronics_products,
        'homegoods_products': homegoods_products
    }

    return render(request, 'admin/addproductpage.html', context)

def uploadproduct(request):
    if request.method == "POST":
        name = request.POST.get('name')
        image = request.FILES['image']
        addcat = request.POST.get('dropdown1')
        desc = request.POST.get('desc')
        form = productmodel(name=name, image=image,addcat=addcat,desc=desc)
        form.save()
        return addproduct(request)
    else:
        return render(request, 'admin/addproductpage.html')
    
def AdminDeleteproduct(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        form = productmodel.objects.get(id=id)
        form.delete()
        return addproduct(request)
    
def AdminDeleteadd(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        form = advertisementmodel.objects.get(id=id)
        form.delete()
        return advertisementpage(request)
    
def view_seo_history(request, user_id):
    user = get_object_or_404(Usermodel, id=user_id)
    search_history = UserSearchHistory.objects.filter(user=user).order_by('-cdate')
    return render(request, 'admin/seo_history.html', {
        'user': user,
        'search_history': search_history
    })
from django.shortcuts import render, redirect
from user.models import *
from django.contrib import messages

from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
import re
from django.utils import timezone
from django.db.models import Q

nltk.download('punkt')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  
    words = nltk.word_tokenize(text)
    return ' '.join(words)

# Create your views here.
def userlogin(request):
    return render(request, 'userlogin.html')

def userregister(request):
    return render(request, 'userregister.html')

def userregisteraction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        pswd = request.POST.get('password')
        phone = request.POST.get('phone')
        form1 = Usermodel(name=name, email=email, password=pswd, phoneno=phone, status='waiting')
        form1.save()
        messages.success(request, 'Registration Successful')
        return render(request, 'userlogin.html')
    else:   
        messages.error(request, 'Registration Un-Successful')
        return render(request, 'userlogin.html')

def userloginaction(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        try:
            check = Usermodel.objects.get(email=email, password=pswd)
            status = check.status
            if status == 'activated':
                request.session['user_id'] = check.id
                return redirect('userhome')
            else:
                messages.error(request, 'Account not activated')
                return render(request, 'userlogin.html')
        except:
            messages.error(request, 'Invalid Login details')
            return render(request, 'userlogin.html')
    else:
        return render(request, 'userlogin.html')
    
def userlogout(request):
    return userlogin(request)

def userhome(request):
    electronics = productmodel.objects.filter(addcat='Electronics').order_by('-created_at')[:4]
    clothing = productmodel.objects.filter(addcat='Clothing').order_by('-created_at')[:4]
    homegoods = productmodel.objects.filter(addcat='Homegoods').order_by('-created_at')[:4]

    return render(request, 'user/userhome.html', {
        'electronics': electronics,
        'clothing': clothing,
        'homegoods': homegoods,
    })

def get_advertisements_by_addcat(addcat):
    return advertisementmodel.objects.filter(addcat=addcat)

def product_details(request, product_id):
    products_details = productmodel.objects.get(id=product_id)
    addcat_variable = products_details.addcat 
    advertisements = get_advertisements_by_addcat(addcat_variable)
    return render(request, 'user/productdetails.html', {'products': products_details, 'adds':advertisements})

def view_more_electronics(request):
    electronics = productmodel.objects.filter(addcat='Electronics').order_by('-created_at')
    return render(request, 'user/view_more.html', {'products': electronics, 'category': 'Electronics'})

def view_more_clothing(request):
    clothing = productmodel.objects.filter(addcat='Clothing').order_by('-created_at')
    return render(request, 'user/view_more.html', {'products': clothing, 'category': 'Clothing'})

def view_more_homegoods(request):
    homegoods = productmodel.objects.filter(addcat='Homegoods').order_by('-created_at')
    return render(request, 'user/view_more.html', {'products': homegoods, 'category': 'Home Goods'})

def usersearches(request):
    user_id = request.session.get('user_id')
    user = Usermodel.objects.get(id=user_id) if user_id else None
    search_history = UserSearchHistory.objects.filter(user=user) if user else []

    context = {
        'search_history': search_history,
    }
    return render(request, 'user/usersearches.html', context)

def product_search(request):
    query = request.GET.get('q')
    top_products = []
    user_id = request.session.get('user_id')
    user = Usermodel.objects.get(id=user_id) if user_id else None
    recommended_products = recommended_ads(user)
    if query:
        if user:
            UserSearchHistory.objects.create(user=user, query=query)

        query = preprocess_text(query)
        query_terms = query.split()
        exact_filter = Q()
        for term in query_terms:
            exact_filter |= Q(name__icontains=term) | Q(desc__icontains=term)
        filtered_products = productmodel.objects.filter(exact_filter)

        if filtered_products.exists():
            products = list(filtered_products)
            product_texts = [preprocess_text(product.name + " " + product.desc) for product in products]

            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([query] + product_texts)

            cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
            related_product_indices = np.argsort(-cosine_similarities)

            top_products = [products[int(idx)] for idx in related_product_indices[:10]]

    else:
        top_products = productmodel.objects.all()

    context = {
        'products': top_products,
        'recommended_products':recommended_products,
    }
    return render(request, 'user/search_results.html', context)

def recommended_ads(user):
    recent_queries = UserSearchHistory.objects.filter(user=user).order_by('-cdate')[:7]
    result_limits = [7, 6, 5, 4, 3, 2, 1]  
    recommended_products = []

    for i, search_history in enumerate(recent_queries):
        query = search_history.query
        query = preprocess_text(query)
        query_terms = query.split()
        exact_filter = Q()

        for term in query_terms:
            exact_filter |= Q(name__icontains=term) | Q(desc__icontains=term)
        filtered_products = productmodel.objects.filter(exact_filter)

        if filtered_products.exists():
            products = list(filtered_products)
            product_texts = [preprocess_text(product.name + " " + product.desc) for product in products]

            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([query] + product_texts)

            cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
            related_product_indices = np.argsort(-cosine_similarities)
            limit = result_limits[i]
            recommended_products.extend([products[int(idx)] for idx in related_product_indices[:limit]])

    return recommended_products
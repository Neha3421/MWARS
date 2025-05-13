"""multiwebsite URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from user import views as usr
from multiwebsite import views as adms

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', adms.index, name='index'),
    path('home/', adms.home, name='home'),
    path('adminlogin/', adms.adminlogin, name='adminlogin'),
    path('adminloginaction/', adms.adminloginaction, name='adminloginaction'),

    path('adminhome/', adms.adminhome, name='adminhome'),
    path('AdminActiveUsers/', adms.AdminActiveUsers, name='AdminActiveUsers'),
    path('advertisementpage/', adms.advertisementpage, name='advertisementpage'),
    path('uploadadd/', adms.uploadadd, name='uploadadd'),
    path('addproduct/',adms.addproduct, name='addproduct'),
    path('uploadproduct/', adms.uploadproduct, name='uploadproduct'),
    path('AdminDeleteproduct/', adms.AdminDeleteproduct, name='AdminDeleteproduct'),
    path('AdminDeleteadd/', adms.AdminDeleteadd, name='AdminDeleteadd'),
    path('adminlogout/', adms.adminlogout, name='adminlogout'),
    path('user/<int:user_id>/seo-history/', adms.view_seo_history, name='view_seo_history'),

    path('userlogin/', usr.userlogin, name='userlogin'),
    path('userloginaction/', usr.userloginaction, name='userloginaction'),
    path('userregister/', usr.userregister, name='userregister'),
    path('userregisteraction/', usr.userregisteraction, name='userregisteraction'),
    path('userhome/', usr.userhome, name='userhome'),
    path('product/<int:product_id>/', usr.product_details, name='product_details'),
    path('userlogout/', usr.userlogout, name='userlogout'),

    path('view_more_electronics/', usr.view_more_electronics, name='view_more_electronics'),
    path('view_more_clothing/', usr.view_more_clothing, name='view_more_clothing'),
    path('view_more_homegoods/', usr.view_more_homegoods, name='view_more_homegoods'),
    path('product_search/', usr.product_search, name='product_search'),
    path('usersearches/', usr.usersearches, name='usersearches'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
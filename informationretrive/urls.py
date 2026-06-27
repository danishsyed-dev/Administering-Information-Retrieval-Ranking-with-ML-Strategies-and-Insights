from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from information.views import *
from user.views import *
from vendor.views import vendor, vendorregistration, vendorloginaction, fileupload, search, usersearchresult, vendor1

urlpatterns = [
    path('', index, name="index"),
    path('index/', index, name="index"),
    path('base/', base, name="base"),
    path('user/', user, name="user"),
    path('userregistration/', userregistration, name="userregistration"),
    path('userloginaction/', userloginaction, name="userloginaction"),
    path('home/', home, name='home'),
    path('search/', search, name="search"),
    path('usersearchresult/', usersearchresult, name="usersearchresult"),
    path('weight/', weight, name="weight"),

    path('vendor/', vendor, name="vendor"),
    path('vendor1/', vendor1, name='vendor1'),
    path('vendorregistration/', vendorregistration, name="vendorregistration"),
    path('vendorloginaction/', vendorloginaction, name="vendorloginaction"),
    path('fileupload/', fileupload, name="fileupload"),

    path('admin/', adminlogin, name="admin"),
    path('adminloginaction/', adminloginaction, name="adminloginaction"),
    path('admin1/', admin1, name="admin1"),
    path('userdetails/', userdetails, name="userdetails"),
    path('vendordetails/', vendordetails, name="vendordetails"),
    path('activateuser/', activateuser, name="activateuser"),
    path('activatevendor/', activatevendor, name="activatevendor"),
    path('filedetails/', filedetails, name="filedetails"),
    path('accurancy/', accurancy, name="accurancy"),
    path('frgt/', frgt, name='frgt'),
    path('nwpwd/', nwpwd, name='nwpwd'),

    path('logout/', logout, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

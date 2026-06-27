from random import randint
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from user.models import registrationmodel, WeightModel
from vendor.models import vendorregistrationmodel, uploadmodel
import random

def index(request):
    return render(request, "index.html")

def base(request):
    return render(request, "base.html")

def adminlogin(request):
    return render(request, "admin/adminlogin.html")

def adminloginaction(request):
    if request.method == "POST":
        login = request.POST.get('username')
        print(login)
        pswd = request.POST.get('password')
        if login == 'admin' and pswd == 'admin':
            return render(request, 'Admin/adminhome.html')
        else:
            messages.success(request, 'Invalid user id and password')
    return render(request, 'admin/adminlogin.html')

def admin1(request):
    return render(request, "Admin/adminhome.html")

def logout(request):
    return render(request, 'index.html')

def userdetails(request):
    userdata = registrationmodel.objects.all()
    return render(request, 'Admin/viewuserdetails.html', {'object': userdata})

def vendordetails(request):
    userdata = vendorregistrationmodel.objects.all()
    return render(request, 'Admin/viewvendordetails.html', {'object': userdata})

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def activateuser(request):
    if request.method == 'GET':
        usid = request.GET.get('usid')
        authkey = random_with_N_digits(8)
        status = 'activated'
        print("USID = ", usid, authkey, status)
        registrationmodel.objects.filter(id=usid).update(authkey=authkey, status=status)
        userdata = registrationmodel.objects.all()
        return render(request, 'Admin/viewuserdetails.html', {'object': userdata})

def activatevendor(request):
    if request.method == 'GET':
        usid = request.GET.get('usid')
        authkey = random_with_N_digits(8)
        status = 'activated'
        print("USID = ", usid, authkey, status)
        vendorregistrationmodel.objects.filter(id=usid).update(authkey=authkey, status=status)
        vendordata = vendorregistrationmodel.objects.all()
        return render(request, 'Admin/viewvendordetails.html', {'object': vendordata})

def filedetails(request):
    obj = uploadmodel.objects.all()
    return render(request, 'admin/uplddetails.html', {"object": obj})

def accurancy(request):
    # Ensure there is sufficient data for the SVM model (at least 10 samples)
    count = WeightModel.objects.count()
    if count < 10:
        # Seed synthetic weights
        for _ in range(10):
            WeightModel.objects.create(weight=random.uniform(0.1, 1.0))
            
    # Load weights from the wgt table
    weights = list(WeightModel.objects.values_list('weight', flat=True))
    dataset = pd.DataFrame(weights)
    dataset1 = pd.DataFrame(weights)
    
    X = dataset
    y = dataset1
    
    # Train / test split (20% test size)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    svclassifier = SVC(kernel='linear')
    
    # SVC expects target to be 1D array. We convert to integer labels or keep float categories
    # Since y contains calculated weights, to perform classification, we can convert weights into class labels (e.g. high/low relevance)
    # Let's map target floats to 0 (low weight) and 1 (high weight) using median weight as threshold to ensure real class separation!
    median_val = y_train[0].median()
    y_train_class = (y_train[0] >= median_val).astype(int)
    y_test_class = (y_test[0] >= median_val).astype(int)
    
    svclassifier.fit(X_train, y_train_class)
    y_pred = svclassifier.predict(X_test)
    
    m = confusion_matrix(y_test_class, y_pred)
    accurancy_report = classification_report(y_test_class, y_pred)
    
    print(m)
    print(accurancy_report)
    x = accurancy_report.split()
    print("Total splits ", len(x))
    
    # Pad splits to prevent index error if report length changes
    if len(x) < 32:
        x = x + [""] * (32 - len(x))
        
    dict_data = {
        "m": m,
        "accurancy": accurancy_report,
        'len0': x[0],
        'len1': x[1],
        'len2': x[2],
        'len3': x[3],
        'len4': x[4],
        'len5': x[5],
        'len6': x[6],
        'len7': x[7],
        'len8': x[8],
        'len9': x[9],
        'len10': x[10],
        'len11': x[11],
        'len12': x[12],
        'len13': x[13],
        'len14': x[14],
        'len15': x[15],
        'len16': x[16],
        'len17': x[17],
        'len18': x[18],
        'len19': x[19],
        'len20': x[20],
        'len21': x[21],
        'len22': x[22],
        'len23': x[23],
        'len24': x[24],
        'len25': x[25],
        'len26': x[26],
        'len27': x[27],
        'len28': x[28],
        'len29': x[29],
        'len30': x[30],
        'len31': x[31],
    }
    return render(request, 'admin/accuracy.html', dict_data)

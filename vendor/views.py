from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from vendor.models import vendorregistrationmodel, uploadmodel
from user.models import registrationmodel
import os

def vendor(request):
    return render(request, 'vendor/vendorlogin.html')

def vendor1(request):
    return render(request, 'vendor/vendorhome.html')

def vendorregistration(request):
    if request.method == 'POST':
        name = request.POST.get('loginid')
        pswd = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        place = request.POST.get('place')
        city = request.POST.get('city')
        
        # Validations
        if not name.isalpha():
            messages.error(request, 'Only strings are allowed for username')
            return render(request, 'vendor/vendorregistration.html')
        if len(mobile) != 10 or not mobile.isdigit():
            messages.error(request, 'Mobile number must be exactly 10 digits')
            return render(request, 'vendor/vendorregistration.html')

        vendorregistrationmodel.objects.create(
            loginid=name,
            password=pswd,
            email=email,
            mobile=mobile,
            place=place,
            city=city,
            authkey='waiting',
            status='waiting'
        )
        messages.success(request, 'You are successfully registered as Vendor')
        return HttpResponseRedirect('/vendor/')
    return render(request, 'vendor/vendorregistration.html')

def vendorloginaction(request):
    if request.method == 'POST':
        usid = request.POST.get('mail')
        pswd = request.POST.get('password')
        try:
            check = vendorregistrationmodel.objects.get(email=usid, password=pswd)
            request.session['vendorid'] = check.loginid
            status = check.status
            if status == "activated":
                request.session['vendor_email'] = check.email
                return render(request, 'vendor/vendorhome.html')
            else:
                messages.success(request, 'Vendor is not activated')
                return render(request, 'vendor/vendorlogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            messages.success(request, 'Invalid vendor id and password')
        return render(request, 'vendor/vendorlogin.html')

def fileupload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            filename = file.name
            # Create pdfs directory if not exists
            pdfs_dir = os.path.join(settings.MEDIA_ROOT, 'files', 'pdfs')
            os.makedirs(pdfs_dir, exist_ok=True)
            
            filepath = os.path.join(pdfs_dir, filename)
            # Save file
            with open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            vendor_name = request.session.get('vendorid', 'Unknown')
            uploadmodel.objects.create(
                filename=filename,
                filepath=os.path.join('files', 'pdfs', filename),
                vendorname=vendor_name
            )
            messages.success(request, 'File uploaded successfully!')
            return render(request, 'vendor/fileupload.html', {'msg': 'File Uploaded Successfully'})
        else:
            messages.error(request, 'Please select a file to upload')
    return render(request, 'vendor/fileupload.html')

def search(request):
    return render(request, 'vendor/search.html')

def usersearchresult(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        # Search by file name or by checking if files contain the search query
        # Since files are text files, we can scan them if we want to do a basic keyword match!
        matched_files = []
        all_uploads = uploadmodel.objects.all()
        
        for upload in all_uploads:
            # Check by filename first
            if query.lower() in upload.filename.lower():
                matched_files.append(upload)
                continue
            
            # Check by text content match
            fPath = os.path.join(settings.MEDIA_ROOT, 'files', 'pdfs', upload.filename)
            if os.path.exists(fPath):
                try:
                    with open(fPath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if query.lower() in content.lower():
                        matched_files.append(upload)
                except Exception:
                    pass
                    
        return render(request, 'vendor/usersearchresult.html', {'object': matched_files, 'query': query})
    return redirect('search')

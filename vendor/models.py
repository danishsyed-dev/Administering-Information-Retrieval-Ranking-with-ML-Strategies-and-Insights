from django.db import models

class vendorregistrationmodel(models.Model):
    loginid = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    authkey = models.CharField(max_length=100, default='waiting')
    status = models.CharField(max_length=100, default='waiting')

    def __str__(self):
        return self.loginid

class uploadmodel(models.Model):
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    vendorname = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

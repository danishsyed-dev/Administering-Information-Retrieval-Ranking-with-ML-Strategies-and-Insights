from django.db import models

class registrationmodel(models.Model):
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

class WeightModel(models.Model):
    weight = models.FloatField()

    class Meta:
        db_table = 'wgt'

    def __str__(self):
        return str(self.weight)

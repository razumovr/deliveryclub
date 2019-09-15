from django.db import models

class Langing(models.Model):
    land=models.CharField(max_length=50)
    success=models.CharField(max_length=50)
    start=models.CharField(max_length=50)
    end=models.CharField(max_length=50)
    complete=models.CharField(max_length=500)
    heshteg=models.CharField(max_length=50)



    #def __str__(self):
        #return self.name

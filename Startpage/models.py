from django.db import models

class Langing(models.Model):
    land=models.CharField(max_length=300)
    success=models.CharField(max_length=300)
    start=models.CharField(max_length=300)
    end=models.CharField(max_length=300)
    complete=models.CharField(max_length=300)
    heshteg=models.CharField(max_length=300)



    #def __str__(self):
        #return self.name

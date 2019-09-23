from django.db import models


class Urlname(models.Model):
    name=models.CharField(max_length=300)

    def __str__(self):
        return self.name



class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)



class Firstvar(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    utm_campaign=models.CharField(max_length=300,null=True)
    utm_term=models.CharField(max_length=300,null=True)
    utm_content=models.CharField(max_length=300,null=True)
    utmname=models.CharField(max_length=300,null=True)

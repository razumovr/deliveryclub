from django.db import models


class Country(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField()

    def __str__(self):
        return self.name


class Person(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class Firstvar(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    utmname=models.CharField(max_length=300)
    def __str__(self):
        return self.name




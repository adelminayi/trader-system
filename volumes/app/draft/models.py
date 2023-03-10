from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=254, unique=True)
    phone = PhoneNumberField()
    comment = models.TextField()
    isAllowed = models.BooleanField(default=False)
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self, *args, **kwargs):
        return self.name + " - " + str(self.phone)


class Coin(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class BuyAndSell(models.Model):
    name = models.CharField(max_length=64)
    coin = models.ManyToManyField(Coin, related_name='buyandsell')

    def __str__(self, *args, **kwargs):
        return self.name
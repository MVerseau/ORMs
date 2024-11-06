from django.db import models

# Create your models here.


class Buyer(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(decimal_places=2, max_digits=9)
    age = models.IntegerField()




class Game(models.Model):
    title = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=8)
    size = models.DecimalField(decimal_places=1, max_digits=4)
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    buyer = models.CharField(max_length=100, default=' ')


from django.db import models
from django.contrib.auth.models import User


class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    full_address = models.CharField(max_length=256)
    
    
class Apartment(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    number = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
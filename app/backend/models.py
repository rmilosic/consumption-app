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
    
class ConsumptionReport(models.Model):
    
    class Type(models.TextChoices):
        APARTMENT = 'Apartment'
        BUILDING = 'Building'
        
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=16, choices=Type.choices)
    season = models.CharField(max_length=16)
    month = models.CharField(max_length=8) 
    period = models.CharField(max_length=32)
    ogr_povrs = models.DecimalField(max_digits=10, decimal_places=2)
    del_ogr_pov = models.DecimalField(max_digits=10, decimal_places=2)
    poraba = models.DecimalField(max_digits=10, decimal_places=2)
    kor_fakt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    osn_pd_13_clen = models.DecimalField(max_digits=10, decimal_places=2)
    korig_pd_15_1_clen = models.DecimalField(max_digits=10, decimal_places=2)
    korig_pd_povrs_15_4_clen = models.DecimalField(max_digits=10, decimal_places=2)
    pod_40_nad_300_18_clen = models.DecimalField(max_digits=10, decimal_places=2)
    prer_pd_100_19_clen = models.DecimalField(max_digits=10, decimal_places=2)
    var_del = models.DecimalField(max_digits=10, decimal_places=2)
    fiks_del = models.DecimalField(max_digits=10, decimal_places=2)
    skp_del_poraba = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class Measurment(models.Model):
    device_number =  models.BigIntegerField()
    space = models.CharField(max_length=64)
    initial_state = models.IntegerField()
    final_state = models.IntegerField()
    corr_factor = models.DecimalField(max_digits=10, decimal_places=2)
    used_units = models.DecimalField(max_digits=10, decimal_places=2)
    consumption_report = models.ForeignKey(ConsumptionReport, on_delete=models.CASCADE)


    

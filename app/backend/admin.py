from django.contrib import admin
from backend.models import Building, Apartment, ConsumptionReport, Measurment


admin.site.register(Building)
admin.site.register(Apartment)
admin.site.register(ConsumptionReport)
admin.site.register(Measurment)
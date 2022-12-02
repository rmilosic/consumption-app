from django.contrib import admin
from backend.models import Building, Apartment, ConsumptionReport, Measurment


class ApartmentAdmin(admin.ModelAdmin):
    list_filter = ['building__full_address']
    list_display = ('id', 'number', 'building', 'owner')
    
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_address')

class ConsumptionReportAdmin(admin.ModelAdmin):
    list_filter = ['type', 'period', 'building', 'month', 'season']
    list_display = ('id', 'type', 'period', 'building', 'apartment', 'month', 'season')

class MeasurmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_number', 'space', 'consumption_report')




admin.site.register(Building, BuildingAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ConsumptionReport, ConsumptionReportAdmin)
admin.site.register(Measurment, MeasurmentAdmin)



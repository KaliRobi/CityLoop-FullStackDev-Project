from django.contrib import admin

from shipmentregister.models import ShipmentDetailsModel
# Register your models here.

class ShipmentregisterAdming(admin.ModelAdmin):
    list_display = ['tracking_number']

admin.site.register(ShipmentDetailsModel)

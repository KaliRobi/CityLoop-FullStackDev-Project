import datetime
from rest_framework import serializers
from .models import ShipmentDetailsModel

class ShipmentRegisterSerialiser(serializers.ModelSerializer):
    

    class Meta:
        model = ShipmentDetailsModel
        read_only_fields = ['tracking_number']
        fields = ['tracking_number', 'origin', 'destination', 'expected_delivery_date', 'mode_of_transport' ]
        

   
    

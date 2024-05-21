import datetime
from rest_framework import serializers
from .models import ShipmentDetailsModel

class ShipmentRegisterSerialiser(serializers.ModelSerializer):
    

    def update(self, instance, validated_data):
        validated_data.pop('tracking_number', None)  
        return super().update(instance, validated_data)

    MOT_OPTIONS = [
        ('Bike', 'Bike'),
        ('Car', 'Car'),
        ('Drone', 'Drone'),
        ('Starship robot', 'Starship robot'),
        ('Truck', 'Truck'),        
        ('Van', 'Van')   
    ]

    trackingNumber = serializers.IntegerField(source='tracking_number')
    origin = serializers.CharField()
    destination = serializers.CharField()
    expectedDeliveryDate = serializers.DateField( source ='expected_delivery_date')
    modeOfTransport = serializers.ChoiceField(
        choices=MOT_OPTIONS,
        source='mode_of_transport'
        )

    class Meta:
        model = ShipmentDetailsModel
        fields = ['trackingNumber', 'origin', 'destination', 'expectedDeliveryDate', 'modeOfTransport' ]
        read_only_fileds = ['trackingNumber']

   
    

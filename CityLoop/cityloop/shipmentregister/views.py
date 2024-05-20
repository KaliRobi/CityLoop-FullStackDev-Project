from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth import logout
from .models import ShipmentDetailsModel
from .serialisers import ShipmentRegisterSerialiser


class GetShipmentView(APIView):

    def get(self, request, tracking_number):
        looked_up_shipment = get_object_or_404(ShipmentDetailsModel, tracking_number=tracking_number)
        serialiser = ShipmentRegisterSerialiser(looked_up_shipment)
        return Response(serialiser.data)

      
class DeleteShipmentView(APIView):

    def delete(self, request, tracking_number):
        shipment_to_delete = get_object_or_404(ShipmentDetailsModel, tracking_number=tracking_number)
        shipment_to_delete.delete()
        return Response(status=status.HTTP_200_OK)
    

class BaseShipmentView(APIView):
    
    def save_serializer(self, serializer):
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CreateShipmentView(BaseShipmentView):

    def post(self, request):
        serialiser = ShipmentRegisterSerialiser(data=request.data)
        if serialiser.is_valid():
            return self.save_serializer(serialiser)
        else:
            return  Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)  
        

class UpdateShipmentView(BaseShipmentView):
       
    def put(self, request, tracking_number):
        shipment_to_update = get_object_or_404(ShipmentDetailsModel, tracking_number=tracking_number)
        serialiser = ShipmentRegisterSerialiser(shipment_to_update, data=request.data)
        if serialiser.is_valid():
            return self.save_serializer(serialiser)
        else:
            return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class ShipmentRegisterListing(generics.ListAPIView):

    serializer_class = ShipmentRegisterSerialiser

    def get_queryset(self):
        queryset = ShipmentDetailsModel.objects.all()
        return queryset
        

class TransportModeView(APIView):

    def get(self, request):
        MOT_OPTIONS = [
            'Bike',
            'Car',
            'Drone',
            'Starship robot',
            'Truck',        
            'Van'   
        ]
        return Response(MOT_OPTIONS)
    





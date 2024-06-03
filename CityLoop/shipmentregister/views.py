from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
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

    
    def save_serializer(self, serializer, request):
        try:
            serializer.save()
            if request.method == 'POST':
                return Response(serializer.data, status=status.HTTP_201_ACCEPTED)
            elif request.method == 'PUT':
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CreateShipmentView(BaseShipmentView):

    
    def post(self, request):
        serialiser = ShipmentRegisterSerialiser(data=request.data)
        if serialiser.is_valid():
            return self.save_serializer(serializer =serialiser, request=request)
        else:
            print('sssss')
            return  Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)  
        

class UpdateShipmentView(BaseShipmentView):

    
    def put(self, request, tracking_number):
        shipment_to_update = get_object_or_404(ShipmentDetailsModel, tracking_number=tracking_number)
        serialiser = ShipmentRegisterSerialiser(shipment_to_update, data=request.data)
        if serialiser.is_valid():
            return self.save_serializer(serializer =serialiser, request=request)
        else:
            print('sssss')
            return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class ShipmentRegisterListing(generics.ListAPIView):

    
    serializer_class = ShipmentRegisterSerialiser
    queryset = ShipmentDetailsModel.objects.all()
        

class TransportModeView(APIView):


    def get(self, request):
        choices = ShipmentDetailsModel.mode_of_transport.field.choices
        return Response([choise[0] for choise in choices] )
    





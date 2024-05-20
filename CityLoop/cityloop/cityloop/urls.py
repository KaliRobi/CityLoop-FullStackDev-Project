from django.contrib import admin
from django.urls import include, path
from shipmentregister.views import DeleteShipmentView, CreateShipmentView, UpdateShipmentView, GetShipmentView, ShipmentRegisterListing
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from shipmentregister.views import TransportModeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', TokenObtainPairView.as_view(), name='token-auth' ),
    path('api-token-auth/refresh/', TokenRefreshView.as_view(), name='token-auth-refresh' ),
    path('shipment/<int:tracking_number>/',  GetShipmentView.as_view(), name='shipment_read'),
    path('shipment/<int:tracking_number>/update/',  UpdateShipmentView.as_view(), name='shipment_update'),
    path('shipment/<int:tracking_number>/delete/',  DeleteShipmentView.as_view(), name='shipment_delete'),
    path('shipment/',  CreateShipmentView.as_view(), name='shipment_create'),
    path('shipment-list/',  ShipmentRegisterListing.as_view(), name='shipment-list'),
    path('transport-modes/', TransportModeView.as_view(), name='transport-modes')
]

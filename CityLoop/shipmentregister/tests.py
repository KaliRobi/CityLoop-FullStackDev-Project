import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import ShipmentDetailsModel
from .views import ShipmentRegisterListing, GetShipmentView, DeleteShipmentView, CreateShipmentView, UpdateShipmentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class TestUrls(TestCase):


    def test_shipment_cud_url(self):
        tracking_number = '123456789' 
        url = reverse('shipment_read', kwargs={'tracking_number': tracking_number})
        self.assertEqual(resolve(url).func.view_class, GetShipmentView)

    def test_shipment_get(self):
        url = reverse('shipment_create')
        self.assertEqual(resolve(url).func.view_class, CreateShipmentView)
    
    def test_shipment_get(self):
        url = reverse('shipment_update')
        self.assertEqual(resolve(url).func.view_class, UpdateShipmentView)

    def test_shipment_get(self):
        tracking_number = '123456789' 
        url = reverse('shipment_delete', kwargs={'tracking_number': tracking_number})
        self.assertEqual(resolve(url).func.view_class, DeleteShipmentView)
        
    def test_shipments_list_url(self):
        url = reverse('shipment-list')
        self.assertEqual(resolve(url).func.view_class, ShipmentRegisterListing)

    def test_user_auth(self):
        url = reverse('token-auth')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_user_auth_refres(self):
        url = reverse('token-auth-refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)


class TesViewsShipmentCrud(TestCase):


    def setUp(self):
        self.client = APIClient()
        self.TEST_SHIPMENT_A = {
    "tracking_number": 456789012,
    "origin": "Uppsala",
    "destination": "Vasteras",
    "expected_delivery_date": "2024-05-23",
    "mode_of_transport": "Car"
}
        self.TEST_SHIPMENT_B = {
    "trackingNumber": 111789012,
    "origin": "Uppsala",
    "destination": "Vasteras",
    "expectedDeliveryDate": "2023-05-23",
    "modeOfTransport": "Bike"
}
        ShipmentDetailsModel.objects.create(
            **self.TEST_SHIPMENT_A
        )

    def test_post_shipment(self):
        response = self.client.post(f'/shipment/', self.TEST_SHIPMENT_B, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['trackingNumber'], 111789012)
       
    def test_post_shipment_again(self):
        response = self.client.post(f'/shipment/', self.TEST_SHIPMENT_B, format='json')
        response_again = self.client.post(f'/shipment/', self.TEST_SHIPMENT_B, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['trackingNumber'], 111789012)
        self.assertEqual(response_again.status_code, 400) 
        
    def test_get_shipment(self):
        response = self.client.get(f'/shipment/{self.TEST_SHIPMENT_A["tracking_number"]}/', format='json' ) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['trackingNumber'], self.TEST_SHIPMENT_A['tracking_number'])

    def test_get_shipment_404(self):
        response = self.client.get(f'/shipment/5678390333/'  ) 
        self.assertEqual(response.status_code, 404)
        
    def test_put_shipment(self):
        data_to_update = self.TEST_SHIPMENT_B.copy()
        data_to_update['destination'] = 'Haapsalu'
        response = self.client.put(f'/shipment/456789012/update/', data_to_update, format='json' )
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['destination'], 'Haapsalu')

    def test_tracking_number_update(self):
        data_to_update = self.TEST_SHIPMENT_B.copy()
        data_to_update['tracking_number'] = 7836287328282
        data_to_update['destination'] = 'Tartu'
        response = self.client.put(f'/shipment/456789012/update/', data_to_update, format='json' )
        self.assertEqual(response.data['trackingNumber'], 456789012)
        self.assertEqual(response.data['destination'], 'Tartu')

    def test_delete_shipment(self):
        TEST_TRACKING_NUMBER = 456789012
        response = self.client.delete(f'/shipment/{TEST_TRACKING_NUMBER}/delete/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ShipmentDetailsModel.objects.all().filter(tracking_number=TEST_TRACKING_NUMBER).exists())
        
        
class TestShipmentRegisterListing(TestCase):


    def setUp(self):
        self.client = APIClient()

        self.TEST_SHIPMENT_A = {
    "tracking_number": 456789012,
    "origin": "Uppsala",
    "destination": "Vasteras",
    "expected_delivery_date": "2024-05-23",
    "mode_of_transport": "Truck"
}
        self.TEST_SHIPMENT_B = {
    "tracking_number": 111789012,
    "origin": "Uppsala",
    "destination": "Vasteras",
    "expected_delivery_date": "2023-05-23",
    "mode_of_transport": "Drone"
}
        ShipmentDetailsModel.objects.create(
            **self.TEST_SHIPMENT_A
        )

        ShipmentDetailsModel.objects.create(
            **self.TEST_SHIPMENT_B
        )

    def test_listing(self):
        response = self.client.get('/shipment-list/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual((response.data['results'][0]['modeOfTransport']), 'Drone')

    def test_delete(self):
        TEST_TRACKING_NUMBER= 111789012
        response = self.client.delete(f'/shipment-list/', format='json')
        self.assertTrue(ShipmentDetailsModel.objects.all().filter(tracking_number=TEST_TRACKING_NUMBER).exists())
        self.assertEqual(response.status_code, 405)
        

class TestUserAuthentication(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='firstname.lastname', password='userpass34565' )
        self.client = APIClient()
        
    def test_can_login(self):
        log_in = self.client.login(username='firstname.lastname', password='userpass34565')
        self.assertTrue(log_in)

    def test_can_not_login(self):
        failed_log_in = self.client.login(username='firstname.lastname', password='userp4565')
        self.assertFalse(failed_log_in)

    def test_gets_jwt(self):
        response = self.client.post('/api-token-auth/', {'username':'firstname.lastname', 'password':'userpass34565'}, format='json')
        self.assertTrue('access' in response.data)
        self.assertEqual(response.status_code, 200)
        

class TestShipmentDetailsModel(TestCase):

    
    def setUp(self):
        self.shipment = ShipmentDetailsModel.objects.create(
            tracking_number=123456,
            origin='Tallinn',
            destination='Tartu',
            expected_delivery_date=datetime.date.today(),
            mode_of_transport='Bike'
        )

    def test_shipment_creation(self):
        self.assertTrue(isinstance(self.shipment, ShipmentDetailsModel))
        self.assertEqual(self.shipment.__str__(), str(self.shipment.tracking_number)) 

    def test_origin(self):
        self.assertEqual(self.shipment.origin, 'Tallinn')

    def test_destination(self):
        self.assertEqual(self.shipment.destination, 'Tartu')

    def test_expected_delivery_date(self):
        self.assertEqual(self.shipment.expected_delivery_date, datetime.date.today())

    def test_mode_of_transport(self):
        self.assertEqual(self.shipment.mode_of_transport, 'Bike')

    def test_field_data_types(self):
        self.assertEqual(type(self.shipment.tracking_number), int)
        self.assertEqual(type(self.shipment.origin), str)
        self.assertEqual(type(self.shipment.destination), str)
        self.assertEqual(type(self.shipment.expected_delivery_date), datetime.date)
        self.assertEqual(type(self.shipment.mode_of_transport), str)

        

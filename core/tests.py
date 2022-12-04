import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from .models import Car, Weight
from .serializers import CarSerializer, WeightSerializer

client = Client()

# --- Weight Test Start


class GetAllWeightTest(TestCase):

    def setUp(self):
        Weight.objects.create(
            type='Curb Weight', unit="lbs", value=4568)
        Weight.objects.create(
            type='Curb Weight 2', unit="lbs", value=44523)
        Weight.objects.create(
            type='Curb Weight 3', unit="lbs", value=2323)
        Weight.objects.create(
            type='Curb Weight 4', unit="lbs", value=5343)

    def test_get_all_weights(self):
        response = client.get(reverse('weights'))
        weights = Weight.objects.all()
        serializer = WeightSerializer(weights, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleWeightTest(TestCase):

    def setUp(self):
        self.foo = Weight.objects.create(
            type='Curb Weight', unit="lbs", value=4568)
        self.foobar = Weight.objects.create(
            type='Curb Weight 2', unit="lbs", value=44523)

    def test_get_valid_single_weight(self):
        response = client.get(
            reverse('weights-detail', kwargs={'pk': self.foobar.pk}))

        weight = Weight.objects.get(pk=self.foobar.pk)
        serializer = WeightSerializer(weight)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_weight(self):
        response = client.get(
            reverse('weights-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewWeightTest(TestCase):

    def setUp(self):
        self.valid_payload = {
            'type': 'Curb Weight',
            'unit': "lbs",
            'value': 4568
        }
        self.invalid_payload = {
            'type': '',
            'unit': "lbs",
            'value': 4568
        }

    def test_create_valid_weight(self):
        response = client.post(
            reverse('weights'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_weight(self):
        response = client.post(
            reverse('weights'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleWeightTest(TestCase):

    def setUp(self):
        self.foo = Weight.objects.create(
            type='Curb Weight', unit="lbs", value=4568)
        self.foobar = Weight.objects.create(
            type='Curb Weight 2', unit="lbs", value=44523)

        self.valid_payload = {
            'type': 'Curb Weight',
            'unit': "lbs",
            'value': 9000
        }
        self.invalid_payload = {
            'type': '',
            'unit': "lbs",
            'value': 4568
        }

    def test_valid_update_weight(self):
        response = client.put(
            reverse('weights-detail', kwargs={'pk': self.foo.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_weight(self):
        response = client.put(
            reverse('weights-detail', kwargs={'pk': self.foo.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleWeightTest(TestCase):

    def setUp(self):
        self.foo = Weight.objects.create(
            type='Curb Weight', unit="lbs", value=4568)
        self.foobar = Weight.objects.create(
            type='Curb Weight 2', unit="lbs", value=44523)

    def test_valid_delete_weight(self):
        response = client.delete(
            reverse('weights-detail', kwargs={'pk': self.foo.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_weight(self):
        response = client.delete(
            reverse('weights-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# --- Weight Test End

# --- Cars Test Start


class GetAllCarsTest(TestCase):

    def setUp(self):
        first_weight = Weight.objects.create(
            type='Curb Weight 1', unit="lbs", value=2000)

        second_weight = Weight.objects.create(
            type='Curb Weight 2', unit="lbs", value=44523)

        Car.objects.create(
            weight=first_weight,
            vin="SCBBR9ZA1AC063223",
            year="2010",
            make="Bentley",
            model="Continental Flying Spur",
            type="Sedan",
            color="Black",
            dimension={
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        )
        Car.objects.create(
            weight=second_weight,
            vin="AVBBR9ZA1AC063223",
            year="2020",
            make="Bentley",
            model="Continental Flying Spur V2",
            type="Sedan",
            color="Black",
            dimension={
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        )

    def test_get_all_cars(self):
        response = client.get(reverse('cars'))
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCarTest(TestCase):

    def setUp(self):
        weight = Weight.objects.create(
            type='Curb Weight 2', unit="lbs", value=44523)

        self.foo = Car.objects.create(
            weight=weight,
            vin="SCBBR9ZA1AC063223",
            year="2010",
            make="Bentley",
            model="Continental Flying Spur",
            type="Sedan",
            color="Black",
            dimension={
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        )
        self.foobar = Car.objects.create(
            weight=weight,
            vin="AVBBR9ZA1AC063223",
            year="2020",
            make="Bentley",
            model="Continental Flying Spur V2",
            type="Sedan",
            color="Black",
            dimension={
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        )

    def test_get_valid_single_car(self):
        response = client.get(
            reverse('cars-detail', kwargs={'pk': self.foobar.pk}))

        car = Car.objects.get(pk=self.foobar.pk)
        serializer = CarSerializer(car)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_car(self):
        response = client.get(
            reverse('cars-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCarTest(TestCase):

    def setUp(self):
        weight = Weight.objects.create(
            type='Curb Weight', unit="lbs", value=44)

        self.valid_payload = {
            "weight": weight.id,
            "vin": "SCBBR9ZA1AC063223",
            "year": "2010",
            "make": "Bentley",
            "model": "Continental",
            "type": "Sedan",
            "color": "Black",
            "dimension": {
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        }
        self.invalid_payload = {
            "weight": {
                "id": 1,
                "type": "Curb Weight 1",
                "unit": "lbs",
                "value": 44523
            },
            "vin": "",
            "year": "",
            "make": "",
            "model": "",
            "type": "",
            "color": "Black",
            "dimension": {
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
            }
        }

    def test_create_valid_car(self):
        response = client.post(
            reverse('cars'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    """ def test_create_invalid_car(self):
        response = client.post(
            reverse('cars'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) """


class UpdateSingleCarTest(TestCase):

    def setUp(self):
        weight = Weight.objects.create(
            type='Curb Weight 1', unit="lbs", value=44523)

        self.foo = Car.objects.create(
            weight=weight,
            vin="SCBBR9ZA1AC063223",
            year="2010",
            make="Bentley",
            model="Continental Flying Spur",
            type="Sedan",
            color="Black",
            dimension={
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        )

        self.valid_payload = {
            "weight": weight.id,
            "vin": "SCBBR9ZA1AC063223",
            "year": "2010",
            "make": "Bentley",
            "model": "Continental",
            "type": "Sedan",
            "color": "Black",
            "dimension": {
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        }
        self.invalid_payload = {
            "weight": {
                "id": 1,
                "type": "Curb Weight 1",
                "unit": "lbs",
                "value": 44523
            },
            "vin": "",
            "year": "2010",
            "make": "Bentley",
            "model": "",
            "type": "Sedan",
            "color": "Black",
            "dimension": {
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
            }
        }

    def test_valid_update_car(self):
        response = client.put(
            reverse('cars-detail', kwargs={'pk': self.foo.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_car(self):
        response = client.put(
            reverse('cars-detail', kwargs={'pk': self.foo.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCarTest(TestCase):

    def setUp(self):
        weight = Weight.objects.create(
            type='Curb Weight 1', unit="lbs", value=44523)

        self.foo = Car.objects.create(
            weight=weight,
            vin="SCBBR9ZA1AC063223",
            year="2010",
            make="Bentley",
            model="Continental Flying Spur",
            type="Sedan",
            color="Black",
            dimension={
                "Wheelbase": "120.70",
                "Rear Legroom": "38.60",
                "Front Legroom": "41.50",
                "Rear Headroom": "37.80",
                "Front Headroom": "36.80",
                "Ground Clearance": "6.00",
                "Track Rear": "63.30",
                "Rear Shoulder Room": "60.40"
            }
        )

    def test_valid_delete_car(self):
        response = client.delete(
            reverse('cars-detail', kwargs={'pk': self.foo.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_car(self):
        response = client.delete(
            reverse('cars-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# --- Cars Test End

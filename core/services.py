import requests
from django.conf import settings
from django.db import transaction
from .models import Car, Weight


def get_decode_vin_code(vim_code: str) -> dict or bool:
    """ Getting decoded information by VIN code """
    decode_request = requests.get(f"{settings.VIN_DECODER}{vim_code}")
    if decode_request.status_code == requests.codes.ok:
        return decode_request.json()
    else:
        return False

def save_decoding_data(decode_data: dict) -> Car:
    """ Saving records with decoded data or returning an error """
    try:
        with transaction.atomic():
            weight = Weight.create(decode_data.get(
                'decode').get('vehicle')[0].get('weight'))
            car = Car.create(decode_data.get('decode'), weight)
        return car
    except Exception:
        raise
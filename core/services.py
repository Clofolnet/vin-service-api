import requests
from django.conf import settings


def get_decode_vin_code(vim_code: str):
    """ Getting decoded information by VIN code """
    vin_service_decoder = settings.VIN_DECODER
    decode_request = requests.get(f"{vin_service_decoder}{vim_code}")
    if decode_request.status_code == requests.codes.ok:
        return decode_request.json()
    else:
        return False

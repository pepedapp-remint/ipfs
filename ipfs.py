import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# NOTE: this file must be added!
from secrets import PINATA_SECRET, PINATA_API_KEY

PIN_JSON_URL = 'https://api.pinata.cloud/pinning/pinJSONToIPFS'
PIN_FILE_URL = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
TEST_AUTH_URL = 'https://api.pinata.cloud/data/testAuthentication'


def test_auth():
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }

    r = requests.get(TEST_AUTH_URL, headers=headers)
    return r


def pin_json(json):
    headers = {
        'Content-Type': 'application/json',
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }

    r = requests.post(PIN_JSON_URL, json=json, headers=headers)
    return r


def pin_file(name, filename):
    with open(filename, 'rb') as f:
        m = MultipartEncoder(
            fields={'file': (name, f)}
        )
        headers = {
            'Content-Type': m.content_type,
            'pinata_api_key': PINATA_API_KEY,
            'pinata_secret_api_key': PINATA_SECRET
        }

        r = requests.post(PIN_FILE_URL, data=m, headers=headers)
        return r

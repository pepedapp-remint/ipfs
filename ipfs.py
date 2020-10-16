import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# NOTE: this file must be added!
from secrets import PINATA_SECRET, PINATA_API_KEY

PIN_JSON_URL = 'https://api.pinata.cloud/pinning/pinJSONToIPFS'
PIN_FILE_URL = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
TEST_AUTH_URL = 'https://api.pinata.cloud/data/testAuthentication'

RESOURCES_DIR = 'resources'
CARDS_DIR = f"{RESOURCES_DIR}/cards"

METADATA_FILE = f"{RESOURCES_DIR}/card_metadata.json"
SIG_TO_HASH_FILE = f"{RESOURCES_DIR}/sig_to_hash.json"


def test_auth():
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }

    r = requests.get(TEST_AUTH_URL, headers=headers)
    return r


def pin_json(name, json):
    headers = {
        'Content-Type': 'application/json',
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }
    payload = {
        'pinataMetadata': {
            'name': name
        },
        'pinataContent': json
    }

    r = requests.post(PIN_JSON_URL, json=payload, headers=headers)
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


def pin_all_cards():
    with open(METADATA_FILE, 'r') as f:
        cards = json.load(f)

    sig_to_ipfs_hash = {}

    for card in cards:
        name = card['name']
        filename = f"{CARDS_DIR}/{card['sig']}.{card['ext']}"
        print(f"[{name}] pinning image file")
        response = pin_file(f"[image] {name}", filename)

        if response.status_code != 200:
            print(f"Error pinning file: {response.text}")
            continue

        response_json = json.loads(response.text)
        ipfs_hash = response_json['IpfsHash']
        print(f"[{name}] image hash: {ipfs_hash}")

        print(f"[{name}] pinning card metadata")
        metadata = {
            'name': name,
            'description': card['description'],
            'image': f"ipfs://ipfs/{ipfs_hash}"
        }
        response = pin_json(f"[metadata] {name}", metadata)

        if response.status_code != 200:
            print(f"Error pinning metadata: {response.text}")

        response_json = json.loads(response.text)
        ipfs_hash = response_json['IpfsHash']
        print(f"[{name}] metadata hash: {ipfs_hash}")
        sig_to_ipfs_hash[card['sig']] = ipfs_hash

    with open(SIG_TO_HASH_FILE, 'w') as f:
        json.dump(sig_to_ipfs_hash, f)

    return sig_to_ipfs_hash

"""Geocode API - address to coordinates."""

import requests
from urllib.parse import quote
from pprint import pprint


def geo_code(address):

    params = {
        "access_token": "pk.eyJ1IjoibHVjaWFuYWN0IiwiYSI6ImNrZnB1NzJzZjAyaTAyc213bzQzaW5xM2IifQ.g-6i_62u4jlDiZbf_kP7ew",
        "fuzzyMatch": "false",
        "types": "address",
    }

    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    full_url = base_url + quote(address) + ".json"

    request = requests.get(full_url, params=params).json()
    # pprint(request)

    list_features = request["features"]
    # print(list_of_features)
    dict_features = list_features[0]
    # print(dict_features)
    list_coordinates = dict_features["center"]  
    # print(list_coordinates)

    coordinates = {"longitude": list_coordinates[0], "latitude": list_coordinates[1]}

    return coordinates
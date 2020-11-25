import requests
from urllib.parse import quote
from pprint import pprint

# request_test = {}


def geo_code(address):

    params = {
        "access_token": "pk.eyJ1IjoibHVjaWFuYWN0IiwiYSI6ImNrZnB1NzJzZjAyaTAyc213bzQzaW5xM2IifQ.g-6i_62u4jlDiZbf_kP7ew",
        "fuzzyMatch": "false",
        "types": "address",
    }

    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

    full_url = base_url + quote(address) + ".json"

    # global request_test
    request_test = requests.get(full_url, params=params).json()

    this_is_list = request_test["features"]
    new_dict = this_is_list[0]
    coordinates = new_dict["center"]  # list

    # pprint(request_test.json())

    final_coordinates = {"longitude": coordinates[0], "latitude": coordinates[1]}

    return final_coordinates

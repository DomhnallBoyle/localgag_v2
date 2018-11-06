from decimal import Decimal
from math import asin, cos, sqrt, pi


# https://stackoverflow.com/a/21623206
def calculate_distance(lat1, long1, lat2, long2):
    """
    Returns the distance between 2 points in KM. Uses the Haversine formula
    :param lat1: Latitude of point 1
    :param long1: Longitude of point 1
    :param lat2: Latitude of point 2
    :param long2: Longitude of point 2
    :return: Distance in km
    """
    p = Decimal(0.017453292519943295)
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((long2 - long1) * p)) / 2

    return 12742 * asin(sqrt(a))

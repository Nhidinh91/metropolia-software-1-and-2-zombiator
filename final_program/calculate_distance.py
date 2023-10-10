from geopy.distance import geodesic
import get_dict_airportcoordinate_by_country


def calculate_distance(current_location, destination):
    dict_airport_coordinate = get_dict_airportcoordinate_by_country.get_dict_airportcoordinate_fromcountry()
    current_coordinate = (dict_airport_coordinate[current_location][0], dict_airport_coordinate[current_location][1])
    destination_coordinate = (dict_airport_coordinate[destination][0], dict_airport_coordinate[destination][1])
    distance = round(geodesic(current_coordinate, destination_coordinate).kilometers,0)
    return distance

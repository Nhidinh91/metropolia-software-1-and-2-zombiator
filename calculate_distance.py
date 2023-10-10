from geopy.distance import geodesic
def calculate_distance(current_location, destination):
    now_location = get_dict_airportcoordinate_by_country(current_location).get(current_location)
    now_destination = get_dict_airportcoordinate_by_country(destination).get(destination)
    distance = geodesic(now_location,now_destination).km
    return distance
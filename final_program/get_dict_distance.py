import get_dict_airportcoordinate_by_country
import calculate_distance as cd
dict_distance = {}
def get_dict_distance(current_location):
    dict_airport = get_dict_airportcoordinate_by_country.get_dict_airportcoordinate_fromcountry()
    for destination in dict_airport:
        if destination != "Finland" and destination != "Spain":
            distance = cd.calculate_distance(current_location, destination)
            dict_distance[destination] = distance
    return dict_distance

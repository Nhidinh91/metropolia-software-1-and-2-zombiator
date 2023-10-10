def list_airport(max_distance,dict_distance):
    for country in dict_distance:
        if dict_distance[country] < max_distance and dict_distance[country] != 0.0:
            print(f"{country} {dict_distance[country]} km")
    return


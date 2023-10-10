import get_dict_distance


def need_more_money(max_distance, current_location):
    dict_distance = get_dict_distance.get_dict_distance(current_location)
    list_distance = []
    for country in dict_distance:
        if dict_distance[country] != 0:
            list_distance.append(dict_distance[country])

    return max_distance < min(list_distance)

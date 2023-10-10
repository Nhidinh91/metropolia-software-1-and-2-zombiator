import get_dict_distance as dis
import random
import dbconnection as db

condition_and_reward = {}
difficult = ["easy", "normal", "hard"]


def need_weapon_and_reward():
    list_country = dis.get_dict_distance("Finland")
    count = 0
    for country in list_country:
        if count == 2 and "hard" in difficult:
            difficult.remove("hard")
        difficult_level = random.choice(difficult)
        if difficult_level == "hard":
            count += 1
        sql = "SELECT name, min_amount, max_amount, difficult_level, passing_condition FROM reward"
        reward = []
        cursor = db.db_connection()
        cursor.execute(sql)
        result = cursor.fetchall()

        if cursor.rowcount > 0:
            reward.append(difficult_level)
            for row in result:
                if row[3] == difficult_level:

                    if row[0] == "money" or row[0] == "weapon":
                        reward.append(random.randint(row[1], row[2]))
                        reward.append(row[4])
            reward.pop(2)
            condition_and_reward[country] = reward
    return condition_and_reward



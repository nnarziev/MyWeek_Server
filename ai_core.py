# region Constants
# map of categories with ids
cat_map = [
    {'loud': 0},
    {'silent': 1},
    {'normal': 2},
    {'alone': 3},
    {'friends': 4},
    {'family': 5},
    {'couple': 6},
    {'adrenaline': 7}
]


# endregion

def ai_predict_time(username, category_id):
    if username != '':
        return category_id
    else:
        return 1

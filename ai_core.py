import random

# region Constants
# map of categories with ids
cat_map = [
    {'name': 'loud', 'code': 0, 'suggestion': 1600},
    {'name': 'silent', 'code': 1, 'suggestion': 2000},
    {'name': 'normal', 'code': 2, 'suggestion': 900},
    {'name': 'alone', 'code': 3, 'suggestion': 1000},
    {'name': 'friends', 'code': 4, 'suggestion': 1400},
    {'name': 'family', 'code': 5, 'suggestion': 2100},
    {'name': 'couple', 'code': 6, 'suggestion': 1900},
    {'name': 'adrenaline', 'code': 7, 'suggestion': 1100}
]


# endregion

def ai_predict_time(username, category_id, json_body):
    el = None
    for _el in cat_map:
        if _el['code'] == category_id:
            el = _el
            break
    if el is None or username is None or username is '':
        return 0

    time = el['suggestion'] + random.randrange(-2, 3, 1) * 100
    return time

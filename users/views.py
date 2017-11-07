from rest_framework.decorators import api_view
from rest_framework.response import Response as Res

from ai_core import advisors, CategoryAdvisor
from users.models import User
import json

# region Constants
RES_SUCCESS = 0
RES_FAILURE = 1
RES_BAD_REQUEST = -1


# endregion


def user_exists(username):
    return User.objects.filter(username=username).exists()


def is_user_valid(username, password):
    if user_exists(username):
        user = User.objects.get(username=username)
        return user.password == password
    return False


@api_view(['POST'])
def handle_login(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' in json_body:
        if is_user_valid(json_body['username'], json_body['password']):
            return Res(data={'result': RES_SUCCESS})
        else:
            return Res(data={'result': RES_FAILURE})
    return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username or Password was not passed as a POST argument!'})


@api_view(['POST'])
def handle_register(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)

    if 'username' in json_body and 'password' in json_body and 'email' in json_body:
        username = json_body['username']
        password = json_body['password']
        email = json_body['email']

        if user_exists(username):
            return Res(data={'result': RES_FAILURE})
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            advisors[user] = CategoryAdvisor.create(None, None)
            return Res(data={'result': RES_SUCCESS})
    else:
        return Res(data={'result': RES_BAD_REQUEST, 'reason': 'Username, or Password was not passed as a POST argument!'})

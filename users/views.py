from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
from users.models import User
import json
from _dummy_thread import error

# region Constants
RES_SUCCESS = 0
RES_FAILURE = 1
RES_BAD_REQUEST = -1


# endregion


def user_exists(_username):
    return User.objects.filter(username=_username).exists()


def is_user_valid(_username, _password):
    if user_exists(_username):
        user = User.objects.get(username=_username)
        return user.password == _password
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
        _username = json_body['username']
        _password = json_body['password']
        _email = json_body['email']
        if user_exists(_username):
            return Res(data={'result': RES_FAILURE})
        else:
            user = User.create(_username, _password, _email)
            try:
                user.save()
                return Res(data={'result': RES_SUCCESS})
            except error:
                return Res(data={'result': RES_FAILURE, 'error': error.__str__()})
    return Res(
        data={'result': RES_BAD_REQUEST, 'reason': 'Email, Username, or Password was not passed as a POST argument!'})

from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
import json

from users.views import is_user_valid, RES_BAD_REQUEST, RES_SUCCESS


@api_view(['POST'])
def create_event(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)

    if is_user_valid(json_body['username'], json_body['password']):
        return Res(data={'result': RES_SUCCESS})
    return Res(data={'result': RES_BAD_REQUEST})

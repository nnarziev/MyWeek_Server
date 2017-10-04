from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
import json
from _dummy_thread import error

from ai_core import ai_predict_time, cat_map
from events.models import Event
from users.views import is_user_valid, RES_BAD_REQUEST, RES_SUCCESS, RES_FAILURE


@api_view(['POST'])
def get_categorycodes(request):
    return Res(data={'result': RES_SUCCESS, 'length': cat_map.__len__(), 'categories': cat_map})


@api_view(['POST'])
def get_events(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']):
        # TODO: get period from request, and get all events in the specific week, then return
        return Res(data={'result': RES_SUCCESS})
    return Res(data={'result': RES_BAD_REQUEST})


@api_view(['POST'])
def get_prediction(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']) and 'category_id' in json_body:
        predicted_time = ai_predict_time(json_body['username'], json_body['category_id'])
        return Res(data={'result': RES_SUCCESS, 'predicted_time': predicted_time})
    else:
        return Res(data={'result': RES_BAD_REQUEST})


@api_view(['POST'])
def create_custom_event(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)

    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']):
        event = Event.create(json_body['username'], json_body['start_time'], json_body['repeat_mode'], json_body['is_active'], json_body['event_name'], json_body['event_note'])
        try:
            event.save()
            return Res(data={'result': RES_SUCCESS, 'event_id': event.event_id})
        except error:
            return Res(data={'result': RES_FAILURE, 'reason': 'Lack of information to create a custom event'})
    else:
        return Res(data={'result': RES_BAD_REQUEST})

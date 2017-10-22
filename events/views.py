import json
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
# from _dummy_thread import error
from ai_core import ai_predict_time, cat_map
from events.models import Event
from users.views import is_user_valid, RES_BAD_REQUEST, RES_SUCCESS, RES_FAILURE

from users.models import User


@api_view(['POST'])
def flushdb(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)

    if 'data' in json_body:
        if 'user' in json_body['data']:
            User.objects.all().delete()
        if 'event' in json_body['data']:
            Event.objects.all().delete()
        return Res(data={'result': 'all done'})
    else:
        return Res(data={'result': 'failed'})


@api_view(['GET', 'POST'])
def get_categorycodes(request):
    arr = []
    for item in cat_map:
        arr.append({item['name']: item['code']})
    return Res(data={'result': RES_SUCCESS, 'categories': arr})


@api_view(['POST'])
def get_suggestion(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']) and 'category_id' in json_body:
        suggestion = ai_predict_time(json_body['username'], json_body['category_id'], json_body)
        rand_day = random.randrange(json_body['today'], json_body['weekend'] + 1, 1)
        suggestion = rand_day * 10000 + suggestion
        return Res(data={'result': RES_SUCCESS, 'suggested_time': suggestion})
    else:
        return Res(data={'result': RES_BAD_REQUEST})


@api_view(['POST'])
def get_events(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']):
        user = User.objects.get(username=json_body['username'])
        _from = json_body['period_from']
        _till = json_body['period_till']
        result = {}
        array = []

        for event in Event.objects.filter(user=user, is_active=True, start_time__gte=_from, start_time__lt=_till):
            array.append(event.__json__())

        result['result'] = RES_SUCCESS
        result['array'] = array
        return Res(data=result)
    return Res(data={'result': RES_BAD_REQUEST})


@api_view(['POST'])
def create_event(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)

    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']):
        user = User.objects.get(username=json_body['username'])

        _leng = json_body['length']
        _from = json_body['start_time']
        # _till = _from + (_leng // 60) * 100 + (_leng % 60)
        # if json_body['repeat_mode'] > 0:  # dynamic event
        #     Event.objects.filter(user=user, is_active=True, start_time__gte=_from, start_time__lt=_till)
        # else:  # static event
        #     asdas
        #
        # if not Event.objects.filter().exists():
        event = Event.objects.create_event(
            user=user,
            repeat_mode=json_body['repeat_mode'],
            start_time=_from,
            length=_leng,
            is_active=True if 'is_active' not in json_body else json_body['is_active'],
            event_name='' if 'event_name' not in json_body else json_body['event_name'],
            event_note='' if 'event_note' not in json_body else json_body['event_note'],
        )
        return Res(data={'result': RES_SUCCESS, 'event_id': event.event_id})
        # else:
        #     return Res(data={'result': RES_FAILURE, 'reason': 'there is an overlapping event in the specified period.'})
    else:
        return Res(data={'result': RES_BAD_REQUEST})


@api_view(['POST'])
def disable_event(request):
    req_body = request.body.decode('utf-8')
    json_body = json.loads(req_body)
    if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']):
        user = User.objects.filter(username=json_body['username'])
        if Event.objects.filter(user=user, event_id=json_body['event_id']).exists():
            event = Event.objects.filter(user=user, event_id=json_body['event_id'])[0]
            if event and event.is_active:
                event.is_active = False
                event.save()
                return Res(data={'result': RES_SUCCESS})
            else:
                return Res(data={'result': RES_FAILURE})
        else:
            return Res(data={'result': RES_FAILURE})
    else:
        return Res(data={'result': RES_BAD_REQUEST})

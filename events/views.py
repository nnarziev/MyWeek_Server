import json
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response as Res
from ai_core import ai_calc_time, Tools
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
	for category in Tools.cat_map:
		arr.append({category['name']: category['id']})
	return Res(data={'result': RES_SUCCESS, 'categories': arr})


@api_view(['POST'])
def get_suggestion(request):
	req_body = request.body.decode('utf-8')
	json_body = json.loads(req_body)
	if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']) and 'category_id' in json_body:
		user = User.objects.get(username=json_body['username'])
		category_id = json_body['category_id']
		suggestion = ai_calc_time(user=user, category_id=category_id)
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

		# TODO: check if there are no overlapping events on the specified period of time

		if 'event_id' in json_body and len(Event.objects.get(event_id=json_body['event_id'], is_active=True)) == 1:
			event = Event.objects.get(event_id=json_body['event_id'], is_active=True)
			event.user = user,
			event.day = json_body['day'] if 'day' in json_body else event.day,
			event.start_time = json_body['start_time'] if 'start_time' in json_body else event.start_time,
			event.length = json_body['length'] if 'length' in json_body else event.length,
			event.is_active = json_body['is_active'] if 'is_active' in json_body else event.is_active,
			event.event_name = json_body['event_name'] if 'event_name' in json_body else event.event_name,
			event.event_note = json_body['event_note'] if 'event_note' in json_body else event.event_note,
			event.category_id = json_body['category_id'] if 'category_id' in json_body else event.category_id
		else:
			event = Event.objects.create_event(
				user=user,
				day=json_body['day'],
				start_time=json_body['start_time'],
				length=json_body['length'],
				is_active=True,
				event_name='' if 'event_name' not in json_body else json_body['event_name'],
				event_note='' if 'event_note' not in json_body else json_body['event_note'],
				category_id=json_body['category_id']
			)
		return Res(data={'result': RES_SUCCESS, 'event_id': event.event_id})
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


@api_view(['POST'])
def populate(request):
	req_body = request.body.decode('utf-8')
	json_body = json.loads(req_body)

	if 'username' in json_body and 'password' in json_body and is_user_valid(json_body['username'], json_body['password']):
		user = User.objects.filter(username=json_body['username'])

		if 'size' in json_body:
			obj_count = Event.objects.filter(user=user).count()

			for category in Tools.cat_map:
				# calculate randomly
				day = category['day'] + random.randrange(-1, 2, 1)
				start_time = category['time'] + random.randrange(-1, 2, 1)

				# verify validity of random calculation
				start_time = start_time if 0 < start_time < 24 else category['start_time']
				day = day if 0 <= day < 7 else category['day']

				for n in range(json_body['size']):
					Event.objects.create_event(user=user, day=day, start_time=start_time, length=60, category_id=category['id'], is_active=False)

			return Res(data={'result': RES_SUCCESS, 'populated': '%d new hidden events' % (Event.objects.filter(user=user).count() - obj_count)})
		else:
			return Res(data={'result': RES_BAD_REQUEST})
	else:
		return Res(data={'result': RES_BAD_REQUEST})

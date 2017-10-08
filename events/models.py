from django.db import models
from django.db.models.deletion import CASCADE
import time


# region Constants
def mode_days(days_count):
    return 'days-' + days_count


def time_ticks():
    return int(round(time.time() * 1000))


# repeat every week on specific days
MODE_REPEAT = 'repeat-xxxxxxx'
# one time event
MODE_SINGLE = 'single'


# endregion Constants


class EventManager(models.Manager):
    def create_event(self, user, repeat_mode, start_time, length, is_active=True, event_name='', event_note=''):
        res = self.create(event_id=time_ticks(), user=user, repeat_mode=repeat_mode, start_time=start_time, length=length, is_active=is_active, event_name=event_name, event_note=event_note)
        return res


class Event(models.Model):
    # the time tick when event created is the event id
    event_id = models.BigIntegerField(primary_key=True, default=0)
    user = models.ForeignKey('users.User', on_delete=CASCADE)
    # format: repeat-(1~127 - in binary format like 1111000), single
    repeat_mode = models.CharField(max_length=9)
    # format: (dynamic on MODE_SINGLE)yymmddhhmm, (static on MODE_REPEAT)hhmm
    start_time = models.IntegerField()
    # in minutes, and only multiple of 30min
    length = models.SmallIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    event_name = models.CharField(max_length=32, default='')
    event_note = models.CharField(max_length=200, default='')
    objects = EventManager()

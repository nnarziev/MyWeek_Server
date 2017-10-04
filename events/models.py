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


class Event(models.Model):
    # the time tick when event created is the event id
    event_id = models.BigIntegerField(primary_key=True, default=0)
    username = models.ForeignKey('users.User', on_delete=CASCADE)
    # format: (dynamic on MODE_SINGLE)yyyymmdd-hhmm, (static on MODE_REPEAT)hhmm
    start_time = models.CharField(max_length=13)
    # format: days-xxxx, repeat, single
    repeat_mode = models.CharField(max_length=9)
    is_active = models.BooleanField
    event_name = models.CharField(max_length=32, default='')
    event_note = models.CharField(max_length=200, default='')

    @classmethod
    def create(cls, _username, _start_time, _repeat_mode, _is_active=True, _event_name='', _event_note=''):
        _event_id = time_ticks()
        res = cls(event_id=_event_id, username=_username, start_time=_start_time, repeat_mode=_repeat_mode, is_active=_is_active, event_name=_event_name, event_note=_event_note)
        return res

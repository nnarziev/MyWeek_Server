from django.db import models
from django.db.models.deletion import CASCADE


# region Constants
def mode_days(days_count):
    return 'days-' + days_count


# repeat every week on specific days
MODE_REPEAT = 'repeat-xxxxxxx'
# one time event
MODE_SINGLE = 'single'


# endregion Constants


class Event(models.Model):
    # the time tick when event created is the event id
    event_id = models.BigIntegerField
    username = models.ForeignKey('users.User', on_delete=CASCADE)
    # format: (dynamic on MODE_SINGLE)yyyymmdd-hhmm, (static on MODE_REPEAT)hhmm
    start_time = models.CharField(max_length=13)
    # format: days-xxxx, repeat, single
    repeat_mode = models.CharField(max_length=16)
    is_active = models.BooleanField
    event_name = models.CharField(max_length=32, primary_key=True, default='')
    event_note = models.CharField(max_length=200, default='')

    @classmethod
    def create(cls, event_id, username, start_time, repeat_mode, is_active=True, event_name='', event_note=''):
        res = cls(event_id, username, start_time, repeat_mode, is_active, event_name, event_note)
        return res

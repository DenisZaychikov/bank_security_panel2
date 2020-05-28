from django.db import models
from django.utils import timezone
import datetime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def get_duration(self):
        if self.leaved_at is None:
            current_time = timezone.localtime()
            entered_at = timezone.localtime(value=self.entered_at)
            delta = (current_time - entered_at).seconds
        else:
            entered_at = timezone.localtime(value=self.entered_at)
            leaved_at = timezone.localtime(value=self.leaved_at)
            delta = (leaved_at - entered_at).seconds

        return delta

    def format_duration(self, duration):
        user_time_in_storage = datetime.timedelta(seconds=duration)
        hours, minutes, _ = (str(user_time_in_storage)).split(':')

        return f'{hours}ч {minutes}мин'

    def is_visit_long(self, minutes=60):
        duration = self.get_duration()
        max_time = datetime.timedelta(minutes=minutes).seconds

        return duration > max_time

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

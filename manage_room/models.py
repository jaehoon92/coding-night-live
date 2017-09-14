import json

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from channels import Group


class Room(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''
    admin_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    admin_user = models.ForeignKey(
        allauth.socialaccount.models.SocialAccount,
        on_delete=models.CASCADE
    )
    '''

    title = models.CharField(max_length=255, default="NoTitle")
    link = models.URLField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        return Group(self.label)

    def send_title(self, new_title):
        self.title = new_title
        self.save()

        final_msg = {
            'rename_title': str(self.label),
            'title': str(self.title),
        }

        self.websocket_group.send({
            "text": json.dumps(final_msg)
        })


class Slide(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=35, default="Unnamed slide")
    md_blob = models.TextField(default="")
    # id : linked list
    now_id = models.AutoField(primary_key=True)
    # if 0 : last element
    next_id = models.PositiveSmallIntegerField(default=0)
    # next_id = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return str(self.now_id)

    @property
    def websocket_group(self):
        return Group(self.room.label)

    def send_idx(self, command):
        # Return idx
        final_msg = {command: str(self.now_id), }

        self.websocket_group.send({
            "text": json.dumps(final_msg)
        })

    def send_title(self):
        # Return idx and title
        final_msg = {
            'rename_slide': str(self.now_id),
            'title': str(self.title)
        }

        self.websocket_group.send({
            "text": json.dumps(final_msg)
        })


class Coworker(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.room.title)

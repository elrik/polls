from __future__ import unicode_literals

from pprint import pprint as pp
import json

from django.http import HttpResponse
from channels import Group
from channels.handler import AsgiHandler
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from channels.routing import route


from .models import Question


@channel_session_user_from_http
def ws_vote(message, poll_id):
    poll = Question.objects.get(pk=poll_id)

    Group(poll.get_channel_group_result()).add(message.reply_channel)

@channel_session_user_from_http
def ws_add(message, poll_id):
    poll = Question.objects.get(pk=poll_id)

    group = Group(poll.get_channel_group_result()).add(message.reply_channel)
    group.send({
        "text": json.dumps(poll.to_dict())
    })

# Connected to websocket.receive
@channel_session_user
def ws_message(message, poll_id):
    poll = Question.objects.get(pk=poll_id)
    group = Group(poll.get_channel_group_result())
    group.send({
        "text": json.dumps(poll.to_dict())
    })

    pp(message.items())
    print poll
    print message['text']

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message, poll_id):
    # print dir(message)
    pp(message.items())
    poll = Question.objects.get(pk=poll_id)
    Group(poll.get_channel_group_result()).discard(message.reply_channel)

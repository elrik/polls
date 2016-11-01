from __future__ import unicode_literals

from pprint import pprint as pp

from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from questionpoll.models import Question


@channel_session_user_from_http
def ws_add(message, poll_id):
    poll = Question.objects.get(pk=poll_id)
    # pp(message.items())

    Group(poll.get_channel_group_result()).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user
def ws_message(message, poll_id):
    print dir(message)
    # poll = Question.objects.get(pk=poll_id)
    # group = Group(poll.get_channel_group_result())

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message, poll_id):
    # print dir(message)
    pp(message.items())
    poll = Question.objects.get(pk=poll_id)
    Group(poll.get_channel_group_result()).discard(message.reply_channel)
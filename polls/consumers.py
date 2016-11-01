from __future__ import unicode_literals

from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http


def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

# @channel_session_user_from_http
def ws_add(message, poll_id):
    print "connecting"
    print message.reply_channel
    # print message.user
    Group("result-1").add(message.reply_channel)

# Connected to websocket.receive
# @channel_session_user
def ws_message(message):
    gg = Group("result-1")
    print gg
    print gg.name
    print gg.channel_layer.alias
    print gg.channel_layer.channel_layer

    gg.send({
        "text": "[user: %s] %s" % (
            # message.user,
            "foo",
            message.content['text'],
        )
    })

# Connected to websocket.disconnect
# @channel_session_user
def ws_disconnect(message):
    # print message.user
    Group("result-1").discard(message.reply_channel)
from __future__ import unicode_literals

from channels.routing import route
from polls.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add, path=r"/(?P<poll_id>\d+)/results/?$"),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
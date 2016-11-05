from channels.routing import route

from .consumers import (
    ws_vote,
    ws_add,
    ws_message,
    ws_disconnect,
)

poll_routing = [
    route("websocket.connect", ws_add, path=r"/(?P<poll_id>\d+)/results/?$"),
    route("websocket.receive", ws_message, path=r"/(?P<poll_id>\d+)/results/?$"),
    route("websocket.disconnect", ws_disconnect, path=r"/(?P<poll_id>\d+)/results/?$"),
    route("websocket.connect", ws_vote, path=r"/(?P<poll_id>\d+)/vote/?$"),
]
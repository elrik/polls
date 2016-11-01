from __future__ import unicode_literals

from channels.routing import include


channel_routing = [
    include("questionpoll.routing.poll_routing", path=r"^"),
]
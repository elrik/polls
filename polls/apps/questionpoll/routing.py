from channels.routing import route, route_class

from .consumers import (
    PollResultsConsumer,
    PollVoteConsumer,
)

poll_routing = [
    route_class(PollResultsConsumer, path=r"/(?P<poll_id>\d+)/results/?$"),
    route_class(PollVoteConsumer, path=r"/(?P<poll_id>\d+)/vote/?$"),
]
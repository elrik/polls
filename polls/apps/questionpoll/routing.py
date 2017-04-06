from channels.routing import route_class

from .consumers import (
    PollResultsConsumer,
    PollVoteConsumer,
    PollEditConsumer,
)

poll_routing = [
    route_class(PollResultsConsumer, path=r"/(?P<poll_id>\d+)/results/?$"),
    route_class(PollVoteConsumer, path=r"/(?P<poll_id>\d+)/vote/?$"),
    route_class(PollEditConsumer, path=r"/(?P<poll_id>\d+)/edit/?$"),
]

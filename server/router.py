from server.handler import Handler


class Route(object):
    name: str
    path: str
    handler: Handler = None


class Router(object):
    prefix: str = None
    route_definition = {}

    pass


class RoutableServer:
    router: Router

    def __init__(self):
        pass

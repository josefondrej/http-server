from queue import Queue
from threading import Thread

from request import Request
from response import Response


class Processor(Thread):
    def __init__(self):
        self._request_queue = Queue()
        self._subscribers = []
        self._actions = dict()
        super().__init__()

    def add_action(self, action_name: str, action):
        self._actions[action_name] = action
        self._actions["/" + action_name] = action

    def add_subscriber(self, subscriber):
        self._subscribers.append(subscriber)

    def enqueue(self, request: Request):
        self._request_queue.put(request)

    def _process(self, request: Request) -> Response:
        try:
            relative_url = request._relative_url
            action_name, raw_args = relative_url.split("?")
            kwargs = raw_args.split("&")
            kwargs = [arg.split("=") for arg in kwargs]
            kwargs = {keyword: value for keyword, value in kwargs}
            action = self._actions[action_name]
            action_result = action(**kwargs)
            content = action_result
        except Exception as e:
            content = str(e)

        response = Response(content, request)
        return response

    def _notify_subscribers(self, response: Response):
        for subscriber in self._subscribers:
            subscriber(response)

    def run(self):
        print("[INFO] Starting processor. ")
        while True:
            request = self._request_queue.get()
            response = self._process(request)
            self._notify_subscribers(response)

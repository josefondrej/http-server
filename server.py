from typing import Callable

from listener import Listener
from logging import log_request
from processor import Processor
from response_queue import ResponseQueue


class Server(object):
    def __init__(self, host: str = "0.0.0.0", port: int = 9494):
        self._processor = Processor()
        self._response_queue = ResponseQueue()
        self._listener = Listener(host, port)

        self._init()

    def _init(self):
        self._listener.add_subscriber(self._processor.enqueue)
        self._listener.add_subscriber(log_request)
        self._processor.add_subscriber(self._response_queue.enqueue)

    def start(self):
        self._processor.start()
        self._response_queue.start()
        self._listener.listen()

    def web(self, action: Callable):
        action_name = action.__name__
        self._processor.add_action(action_name, action)

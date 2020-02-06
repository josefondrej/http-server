from queue import Queue
from threading import Thread

from response import Response
from sender import Sender


class ResponseQueue(Thread):
    def __init__(self, pool_size: int = 10):
        self._pool_size = pool_size
        self._response_queue = Queue()

        super().__init__()

    def enqueue(self, response: Response):
        self._response_queue.put(response)

    def run(self):
        for i in range(self._pool_size):
            sender = Sender(self._response_queue)
            sender.start()

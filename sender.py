from queue import Queue
from threading import Thread

from response import Response


class Sender(Thread):
    def __init__(self, response_queue: Queue):
        self._response_queue = response_queue
        super().__init__()

    def _send(self, response: Response):
        serialized_response = response.serialize()
        client_socket = response.client_socket

        client_socket.send(serialized_response)
        client_socket.close()

    def run(self):
        while True:
            response = self._response_queue.get()
            self._send(response)

import socket

from downloader import Downloader


class Listener(object):
    def __init__(self, host: str = "0.0.0.0", port: int = 9494):
        self._host = host
        self._port = port
        self._subscribers = []
        self._init()

    def _init(self):
        self._listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Aby se mohl hned znovupouzit kdyz se na nem ukonci spojeni
        self._listening_socket.bind((self._host, self._port))  # Porty nizsi nez 1024 muzou chtit root
        self._listening_socket.listen()  # Call na system, kdyz tam neco prijde tak to preda

    def add_subscriber(self, function):
        self._subscribers.append(function)

    def _notify_subscribers(self, request):
        for subscriber in self._subscribers:
            subscriber(request)

    def listen(self):
        print("[INFO] Starting listener.")
        while True:
            client_socket, address = self._listening_socket.accept()  # socket.socket.accept() vraci socket.socket
            downloader = Downloader(client_socket, address)
            downloader._on_request_accepted = self._notify_subscribers

            downloader.start()

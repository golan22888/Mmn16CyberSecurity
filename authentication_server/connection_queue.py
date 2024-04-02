from threading import Lock, Condition


class ConnectionQueue:
    def __init__(self):
        self.lock = Lock()
        self.connections = []
        self.condition = Condition()

    def add_connection(self, request):
        with self.condition:
            with self.lock:
                self.connections.append(request)

            self.condition.notify()

    def get_connection(self):
        with self.condition:
            while not self.connections:
                self.condition.wait()

            with self.lock:
                return self.connections.pop(0)

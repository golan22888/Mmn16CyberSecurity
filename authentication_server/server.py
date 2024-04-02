import socket
from request_handler import RequestHandler
from connection_queue import ConnectionQueue
from servers_mutual_key import get_key_from_file

SERVERS_MUTUAL_KEY = get_key_from_file()


class Server:
    def __init__(self, port, clients_manager):
        try:
            self.port = port
            self.clients_manager = clients_manager
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('localhost', self.port))
            self.connections_queue = ConnectionQueue()
        except Exception as e:
            raise Exception('Error connecting to socket by authentication server')

    def start(self):
        try:
            RequestHandler(self.connections_queue, self.clients_manager).start()

            self.socket.listen()
            print(f'Server listening on port {self.port}')

            while True:
                client_socket, client_address = self.socket.accept()
                self.connections_queue.add_connection((client_socket, client_address))
        except Exception as e:
            print(e)
            raise Exception('Error connecting to authentication server')

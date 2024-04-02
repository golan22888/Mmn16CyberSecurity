import socket
# from requests_handler import RequestHandler


class Client:
    def __init__(self, port):
        try:
            self.port = port
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('localhost', self.port))
            
        except Exception as e:
            raise Exception('Error connecting to socket by client')



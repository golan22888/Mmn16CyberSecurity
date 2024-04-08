import socket
import struct
from message import Message
from response_serializer import ResponseSerializer
from request_parser import RequestParser

CLIENT_VERSION = 24
PACKET_SIZE = 1024
SERVER_HEADER_SIZE = 7


class Connection:
    def __init__(self, address, port):
        self.address = address
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.address, self.port))
            return True
        except Exception as e:
            print(e)
            print('Error while connecting to {}:{}'.format(self.address, self.port))
            return False

    def disconnect(self):
        self.socket.close()

    def send(self, message):
        try:
            serialized_message = ResponseSerializer.serialize(message)
            self.socket.sendall(serialized_message)
            return True
        except Exception as e:
            print(e)
            print('Error while sending to {}:{}'.format(self.address, self.port))
            return False

    def receive(self):
        try:
            data = b''
            while len(data) < SERVER_HEADER_SIZE:
                buffer = self.socket.recv(PACKET_SIZE)
                data += buffer

            header_data = data[:SERVER_HEADER_SIZE]
            header = RequestParser.parse_header(header_data)
            if header.code == 1609:
                raise Exception("server responded with an error")
            payload_size = header.get_payload_size()

            while len(data) < payload_size:
                buffer = self.socket.recv(PACKET_SIZE)
                data += buffer

            payload_data = data[SERVER_HEADER_SIZE: SERVER_HEADER_SIZE + payload_size]
            payload = RequestParser.parse_payload(header.get_code(), payload_data)

            request = Message(header, payload)

            return request

        except Exception as e:
            print(e)
            raise Exception('Error while receiving request')


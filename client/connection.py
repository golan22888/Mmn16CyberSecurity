import socket
import struct
from message import Message

CLIENT_VERSION = 24
PACKET_SIZE = 1024


class Connection:
    def __init__(self, address, port):
        self.address = address
        self.port = port
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
            client_id_size = 16
            protocol_msg_format = f'< {client_id_size}s B H I {message.get_header().get_payload_size()}'
            msg_data = struct.pack(protocol_msg_format, message)
            self.socket.sendall(msg_data)
            return True
        except Exception as e:
            print(e)
            print('Error while sending to {}:{}'.format(self.address, self.port))
            return False

    def receive(self):
        PROTOCOL_HEADER_FORMAT = '< B H I'
        try:
            header_buffer = self.socket.recv(7)
            version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, header_buffer)
            payload = b''
            while len(payload) < payload_size:
                buffer = self.socket.recv(PACKET_SIZE)
                if not buffer:
                    raise RuntimeError('Error while receiving packet')
                payload += buffer
            message = Message(header_buffer, payload)
            return message
        except Exception as e:
            print(e)
            return None

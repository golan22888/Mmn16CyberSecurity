from threading import Thread
from handler_provider import HandlerProvider
from response_provider import ResponseProvider
from response_serializer import ResponseSerializer
from message import Message
from request_parser import RequestParser
from header_parser import HEADER_SIZE

PACKET_SIZE = 1024


class RequestHandler(Thread):
    def __init__(self, connections_queue, client_manager):
        super().__init__()
        self.connections_queue = connections_queue
        self.client_manager = client_manager

    def run(self):
        while True:
            client_socket, client_address = self.connections_queue.get_connection()

            print(f'handling connction from {client_address}\n')
            Thread(target=self.handle_request, args=(client_socket, )).start()

    def handle_request(self, socket):
        while True:
            try:
                request = self.receive_request(socket)
                request_handler = HandlerProvider.get_request_handler(request.get_header().get_code())
                response = request_handler.handle(request, self.client_manager)
            except Exception as e:
                print(e)
                response = ResponseProvider.make_response(None, 1609)

            serialized_response = self.serialize_response(response)
            self.send_response(serialized_response, socket)

    @staticmethod
    def receive_request(socket):
        try:
            data = b''

            while len(data) < HEADER_SIZE:
                buffer = socket.recv(PACKET_SIZE)
                data += buffer

            header_data = data[:HEADER_SIZE]
            header = RequestParser.parse_header(header_data)
            payload_size = header.get_payload_size()

            while len(data) < payload_size:
                buffer = socket.recv(PACKET_SIZE)
                data += buffer

            payload_data = data[HEADER_SIZE: HEADER_SIZE + payload_size]
            payload = RequestParser.parse_payload(header.get_code(), payload_data)

            request = Message(header, payload)

            return request

        except Exception as e:
            print(e)
            raise Exception('Error while recieving request')

    @staticmethod
    def serialize_response(response):
        if response:
            try:
                return ResponseSerializer.serialize(response)
            except Exception as e:
                print(e)
                raise Exception('Error while serializing response')

    @staticmethod
    def send_response(serialized_response, socket):
        if serialized_response:
            try:
                socket.send(serialized_response)
            except Exception as e:
                print(e)
                raise Exception('Error while sending response')
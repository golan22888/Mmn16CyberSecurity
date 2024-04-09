import uuid

from authenticator import Authenticator
from connection import Connection
import me
from header import ResponseHeader
import payload as p
from message import Message
from Crypto.Random import get_random_bytes

CLIENT_VERSION = 24
SERVER_ID = '1066b629bebc4c3d9f236c33c013e084'
NONCE_SIZE = 8


class Client:
    def __init__(self, auth_server_ip, auth_server_port, msg_server_ip, msg_server_port):
        self.auth_server_ip = auth_server_ip
        self.auth_server_port = auth_server_port
        self.msg_server_ip = msg_server_ip
        self.msg_server_port = msg_server_port

    def start(self):
        connection_auth = Connection(self.auth_server_ip, self.auth_server_port)
        connection_auth.connect()
        success, client_name, client_id = me.get_client_info()
        while not success:
            client_name = self.register(connection_auth)
            response_from_server = connection_auth.receive()
            if response_from_server.get_header().get_code() == 1601:
                print("User with that name is already exist")
                continue
            success = True
            client_id = response_from_server.get_payload().get_client_id()
            me.add_to_me_info(client_name, client_id)

        nonce = self.ask_for_key_and_ticket(client_id, connection_auth)
        response_from_server = connection_auth.receive()
        try:
            self.check_code(response_from_server.get_header().get_code(), 1603)
        except Exception as e:
            print(e)
        decrypted_key = response_from_server.get_payload().get_decrypted_key()

        # check if the nonce value form the server is valid
        try:
            self.check_nonce(decrypted_key.get_nonce(), nonce)
        except Exception as e:
            print(e)
        authenticator = Authenticator(response_from_server.get_header().get_version(), client_id, SERVER_ID,
                                      decrypted_key.get_client_and_mag_server_aes_key())
        connection_auth.disconnect()

        # start communication with message server
        connection_msg = Connection(self.msg_server_ip, self.msg_server_port)
        connection_msg.connect()
        self.send_authenticator_and_ticket(client_id, authenticator, response_from_server.get_payload().get_ticket(),
                                           connection_msg)

        response_from_server = connection_msg.receive()
        try:
            self.check_code(response_from_server.get_header().get_code(), 1604)
        except Exception as e:
            print(e)

        self.send_msg_to_print(client_id, decrypted_key.get_client_and_mag_server_aes_key(), connection_msg)
        response_from_server = connection_msg.receive()
        try:
            self.check_code(response_from_server.get_header().get_code(), 1605)
        except Exception as e:
            print(e)

    def register(self, connection):
        name = input("Enter your username: ")
        password = input("Enter your password: ")
        self.make_registration_request(name, password, connection)
        return name

    @staticmethod
    def make_registration_request(name, password, connection):
        client_id = uuid.uuid4()
        header = ResponseHeader(client_id, CLIENT_VERSION, 1024)
        payload = p.SendNameAndPassPayload(name, password)
        response = Message(header, payload)
        connection.send(response)

    @staticmethod
    def ask_for_key_and_ticket(client_id, connection):
        nonce = get_random_bytes(NONCE_SIZE)
        header = ResponseHeader(client_id, CLIENT_VERSION, 1027)
        payload = p.SendServerIdAndNoncePayload(SERVER_ID, nonce)
        response = Message(header, payload)
        connection.send(response)
        return nonce

    @staticmethod
    def send_authenticator_and_ticket(client_id, authenticator, ticket, connection):
        header = ResponseHeader(client_id, CLIENT_VERSION, 1028)
        payload = p.SendAuthenticatorAndTicketPayload(authenticator, ticket)
        response = Message(header, payload)
        connection.send(response)

    @staticmethod
    def check_nonce(nonce1, nonce2):
        if nonce1 != nonce2:
            raise Exception("invalid nonce")

    @staticmethod
    def check_code(code1, code2):
        if code1 != code2:
            raise Exception("received a code from the server that was not expected")

    @staticmethod
    def send_msg_to_print(client_id, decrypted_key, connection):
        message_content = input("Enter your message: ")
        header = ResponseHeader(client_id, CLIENT_VERSION, 1029)
        payload = p.SendMessagePayload(message_content, decrypted_key)
        response = Message(header, payload)
        connection.send(response)

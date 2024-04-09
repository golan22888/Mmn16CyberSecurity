from abc import ABC, abstractmethod
from crypt import generate_aes_key
from response_provider import ResponseProvider
from encrypted_key import EncryptedKey
from ticket import Ticket

SERVER_VERSION = 24


class Handler(ABC):
    @staticmethod
    @abstractmethod
    def handle(request, client_manager):
        pass


class RegisterHandler(Handler):
    @staticmethod
    def handle(request, client_manager):
        try:
            if SERVER_VERSION != request.get_header().get_version():
                raise Exception
            client_name = request.get_payload().get_name()
            client_password = request.get_payload().get_password()
            client = client_manager.get_client_by_name(client_name)

            if client:
                return ResponseProvider.make_response(request, 1601)

            client_manager.register_client(client_name, client_password)
            client = client_manager.get_client_by_name(client_name)
            print(f'client {client_name} is registered')
            return ResponseProvider.make_response(request, 1600, client_id=client.get_client_id())
        except Exception as e:
            print(e)
            ResponseProvider.make_response(request, 1609)
            raise Exception('failed to register client')


class SymKeyRequestHandler(Handler):
    @staticmethod
    def handle(request, client_manager):
        try:
            if SERVER_VERSION != request.get_header().get_version():
                raise Exception
            client_id = request.get_header().get_client_id()
            server_id = request.get_payload().get_server_id()
            nonce = request.get_payload().get_nonce()
            aes_key = generate_aes_key()
            encrypted_key = EncryptedKey(nonce, aes_key, client_manager.get_client_by_id(client_id))
            ticket = Ticket(client_id, server_id, aes_key)

            return ResponseProvider.make_response(request, 1603, client_id=client_id, encrypted_key=encrypted_key,
                                                  ticket=ticket)

        except Exception as e:
            print(e)
            ResponseProvider.make_response(request, 1609)
            raise Exception('Error while sending the symmetric key and the ticket')

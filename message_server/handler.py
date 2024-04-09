from abc import ABC, abstractmethod

from client import Client
from response_provider import ResponseProvider
from crypt import decrypt_aes_cbc as decrypt


SERVER_VERSION = 24


class Handler(ABC):
    @staticmethod
    @abstractmethod
    def handle(request, client_manager):
        pass


class SentSymKeyHandler(Handler):
    @staticmethod
    def handle(request, client_manager):
        try:
            if SERVER_VERSION != request.get_header().get_version():
                raise Exception
            client_id = request.get_header().get_client_id()
            client_key = request.get_payload().get_ticket().get_decrypted_client_and_msg_server_aes_key()
            client_expiration_time = request.get_payload().get_ticket().get_decrypted_expiration_time()
            client = Client(client_id, client_key, client_expiration_time)
            client_manager.save_client(client)
            print(f'client {client_id} is sending a symmetric key')
            return ResponseProvider.make_response(request, 1604)
        except Exception as e:
            print(e)
            ResponseProvider.make_response(request, 1609)
            raise Exception('failed to get client symmetric key')


class SentMessageHandler(Handler):
    @staticmethod
    def handle(request, client_manager):
        try:
            if SERVER_VERSION != request.get_header().get_version():
                raise Exception
            client_id = request.get_header().get_client_id()
            client = client_manager.get_client_by_id(client_id)
            if client.key_is_expired():
                raise Exception
            msg_iv = request.get_payload().get_message_iv()
            encrypted_message = request.get_payload().get_message_content()
            client_key = client.get_client_msg_server_key()
            decrypted_message = decrypt(client_key, encrypted_message, msg_iv)
            # need to print message after decrypting it
            print(f'client {client_id} is sent this message:')
            print(decrypted_message)
            return ResponseProvider.make_response(request, 1605)
        except Exception as e:
            print(e)
            ResponseProvider.make_response(request, 1609)
            raise Exception('Error while printing the message of client')



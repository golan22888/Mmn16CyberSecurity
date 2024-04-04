from abc import ABC, abstractmethod
import struct

SERVER_ID_SIZE = CLIENT_ID_SIZE = 16
AUTHENTICATOR_IV_SIZE = TICKET_IV_SIZE = MESSAGE_IV_SIZE = 16
AES_KEY_SIZE = 32
VERSION_SIZE = 1
EXPIRATION_TIME_SIZE = CREATION_TIME_SIZE = 8
AES_CBC_BLOCK_SIZE = 16


class PayloadSerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(payload):
        pass


class SymKeyPayloadSerializer(PayloadSerializer):
    # version, client_id, server_id, creation_time, aes_key, expiration_time -> those arguments are encrypted so we
    # need to get them with their padding
    PROTOCOL_PAYLOAD_FORMAT = (
        f'< {AUTHENTICATOR_IV_SIZE}s {AES_CBC_BLOCK_SIZE} {AES_CBC_BLOCK_SIZE}s {AES_CBC_BLOCK_SIZE}s '
        f'{AES_CBC_BLOCK_SIZE}s B {CLIENT_ID_SIZE}s {SERVER_ID_SIZE}s {CREATION_TIME_SIZE}s {TICKET_IV_SIZE}s '
        f'{2 * AES_CBC_BLOCK_SIZE}s {AES_CBC_BLOCK_SIZE}s')

    @staticmethod
    def serialize(payload):
        authenticator = payload.get_authenticator()
        ticket = payload.get_ticket()
        serialized_payload = struct.pack(SymKeyPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT,
                                         authenticator.get_authenticator_iv(), authenticator.get_version(),
                                         authenticator.get_client_id(), authenticator.get_server_id(),
                                         authenticator.get_creation_time(), ticket.get_version(),
                                         ticket.get_client_id(), ticket.get_server_id(), ticket.get_creation_time(),
                                         ticket.get_ticket_iv(), ticket.get_encrypted_aes_key(),
                                         ticket.get_encrypted_expiration_time())
        return serialized_payload


class MsgPayloadSerializer(PayloadSerializer):
    PROTOCOL_PAYLOAD_FORMAT = f'< I {MESSAGE_IV_SIZE}s'
    @staticmethod
    def serialize(payload):
        message = payload.get_message()
        message_iv = payload.get_message_iv()
        message_content = payload.get_message_content()

        serialized_payload = struct.pack()

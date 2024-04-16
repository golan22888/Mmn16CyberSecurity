from abc import ABC, abstractmethod
import struct
import base64
from authenticator_constant import CLIENT_ID_SIZE, ENCRYPTED_KEY_IV_SIZE, SERVER_ID_SIZE, TICKET_IV_SIZE, \
    AES_CBC_BLOCK_SIZE


class PayloadSerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(payload):
        pass


class EmptyPayloadSerializer(PayloadSerializer):
    @staticmethod
    def serialize(payload):
        return b''


class RegisterPayloadSerializer(PayloadSerializer):
    PROTOCOL_PAYLOAD_FORMAT = f'< {CLIENT_ID_SIZE}s'

    @staticmethod
    def serialize(payload):
        client_id = payload.get_client_id()
        serialized_payload = struct.pack(RegisterPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id.bytes)

        return serialized_payload


class RequestSymKeyPayloadSerializer(RegisterPayloadSerializer):
    PROTOCOL_PAYLOAD_FORMAT = (
        # nonce, aes_key, aes_key, expiration_time -> those arguments are encrypted, so we need to get them with the
        # padded data
        f'< {CLIENT_ID_SIZE}s {ENCRYPTED_KEY_IV_SIZE}s {AES_CBC_BLOCK_SIZE}s {3 * AES_CBC_BLOCK_SIZE}s '
        f' B {CLIENT_ID_SIZE}s {SERVER_ID_SIZE}s d '
        f'{TICKET_IV_SIZE}s {3 * AES_CBC_BLOCK_SIZE}s {AES_CBC_BLOCK_SIZE}s')

    @staticmethod
    def serialize(payload):
        client_id = payload.get_client_id()
        encrypted_key = payload.get_encrypted_key()
        ticket = payload.get_ticket()
        serialized_payload = struct.pack(RequestSymKeyPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id.bytes,
                                         base64.b64decode(encrypted_key.get_encrypted_key_iv()),
                                         base64.b64decode(encrypted_key.get_nonce()),
                                         base64.b64decode(encrypted_key.get_encrypted_key()), ticket.get_version(),
                                         ticket.get_client_id().bytes, ticket.get_server_id(),
                                         ticket.get_creation_time(),
                                         base64.b64decode(ticket.get_ticket_iv()),
                                         base64.b64decode(ticket.get_encrypted_aes_key()),
                                         base64.b64decode(ticket.get_encrypted_expiration_time()))

        return serialized_payload

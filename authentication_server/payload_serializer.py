from abc import ABC, abstractmethod
import struct

from Crypto.Cipher import AES

VERSION_SIZE = 1
NONCE_SIZE = 8
EXPIRATION_TIME_SIZE = CREATION_TIME_SIZE = 8
SERVER_ID_SIZE = CLIENT_ID_SIZE = 16
ENCRYPTED_KEY_IV_SIZE = TICKET_IV_SIZE = 16
AES_KEY_SIZE = 32
ENCRYPTED_KEY_SIZE = ENCRYPTED_KEY_IV_SIZE + NONCE_SIZE + AES_KEY_SIZE
TICKET_SIZE = (VERSION_SIZE + CLIENT_ID_SIZE + SERVER_ID_SIZE + CREATION_TIME_SIZE + TICKET_IV_SIZE + AES_KEY_SIZE +
               EXPIRATION_TIME_SIZE)
AES_CBC_BLOCK_SIZE = 16


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
        f'< {CLIENT_ID_SIZE}s {ENCRYPTED_KEY_IV_SIZE}s {AES_CBC_BLOCK_SIZE}s {2 * AES_CBC_BLOCK_SIZE}s '
        f'{VERSION_SIZE}s {CLIENT_ID_SIZE}s {SERVER_ID_SIZE}s {CREATION_TIME_SIZE}s '
        f'{TICKET_IV_SIZE}s {2 * AES_CBC_BLOCK_SIZE}s {AES_CBC_BLOCK_SIZE}s')

    @staticmethod
    def serialize(payload):
        client_id = payload.get_client_id()
        encrypted_key = payload.get_encrypted_key()
        ticket = payload.get_ticket()
        serialized_payload = struct.pack(RequestSymKeyPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id,
                                         encrypted_key.get_encrypted_key_iv(), encrypted_key.get_nonce(),
                                         encrypted_key.get_encrypted_key(), ticket.get_version(),
                                         ticket.get_client_id(), ticket.get_server_id(), ticket.get_creation_time(),
                                         ticket.get_ticket_iv(), ticket.get_encrypted_aes_key(),
                                         ticket.get_encrypted_expiration_time())

        return serialized_payload

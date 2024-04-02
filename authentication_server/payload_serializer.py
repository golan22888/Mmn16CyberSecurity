from abc import ABC, abstractmethod
import struct

SERVER_ID_SIZE = CLIENT_ID_SIZE = 16
ENCRYPTED_KEY_IV_SIZE = TICKET_IV_SIZE = 16
NONCE_SIZE = 8
AES_KEY_SIZE = 32
VERSION_SIZE = 1
EXPIRATION_TIME_SIZE = CREATION_TIME_SIZE = 8
ENCRYPTED_KEY_SIZE = ENCRYPTED_KEY_IV_SIZE + NONCE_SIZE + AES_KEY_SIZE
TICKET_SIZE = (VERSION_SIZE + CLIENT_ID_SIZE + SERVER_ID_SIZE + CREATION_TIME_SIZE + TICKET_IV_SIZE + AES_KEY_SIZE +
               EXPIRATION_TIME_SIZE)


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
    PROTOCOL_PAYLOAD_FORMAT = f'< {CLIENT_ID_SIZE}s {ENCRYPTED_KEY_SIZE}s {TICKET_SIZE}'

    @staticmethod
    def serialize(payload):
        client_id = payload.get_client_id()
        encrypted_key = payload.get_encrypted_key()
        ticket = payload.get_ticket()
        serialized_payload = struct.pack(RequestSymKeyPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, client_id,
                                         encrypted_key, ticket)

        return serialized_payload
